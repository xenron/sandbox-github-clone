from django.core.management.base import BaseCommand
from django.db.models import Case, When, Value, Sum, IntegerField, CharField
from libs.dump import dump_sql
from apps.runner.models import Book

class Command(BaseCommand):
    # manage.pyで動作させた時に引数を受け取れるようにする
    args = '引数'

    def handle(self, *args, **options):
        if 'when' in args:
            self.case_when()

        if 'sum' in args:
            self.case_sum()


    def case_when(self):
        # name列とcase式で作成したimpression列を表示
        b = Book.objects.annotate(
            impression=Case(
                When(pages=10, then=Value('short')),
                When(pages=20, then=Value('short')),
                When(pages=30, then=Value('good')),
                When(pages=40, then=Value('long')),
                default=Value('nothing'),
                output_field=CharField()
            )
        ).values('name', 'impression')
        #=> SELECT "runner_book"."name",
        #     CASE WHEN "runner_book"."pages" = %s THEN %s
        #          WHEN "runner_book"."pages" = %s THEN %s
        #          WHEN "runner_book"."pages" = %s THEN %s
        #          WHEN "runner_book"."pages" = %s THEN %s
        #          ELSE %s END AS "impression"
        #   FROM "runner_book"
        #   LIMIT 21' - PARAMS = (10, 'short', 20, 'short', 30, 'good', 40, 'long', 'nothing')

        print(b)
        dump_sql()


    def case_sum(self):
        # ratingが3より大きい本のうち、ratingごとに、出版社1・出版社2別の冊数を算出する
        # インスパイア: [CASE式のススメ](http://www.geocities.jp/mickindex/database/db_case.html)

        b = Book.objects.values('rating').filter(rating__gt=3).annotate(
            # defalutがあるので、then=0はいらないけど、見栄え上残しておく
            pub1=Sum(Case(
                When(rating=5, then=1),
                When(rating=4, then=0),
                default=Value(0),
                output_field=IntegerField()
            )),
            pub2=Sum(Case(
                When(rating=5, then=0),
                When(rating=4, then=1),
                default=Value(0),
                output_field=IntegerField()
            ))
        )
        #=> SELECT "runner_book"."rating",
        #          SUM(CASE WHEN "runner_book"."rating" = %s THEN %s
        #                   WHEN "runner_book"."rating" = %s THEN %s ELSE %s END) AS "pub2",
        #          SUM(CASE WHEN "runner_book"."rating" = %s THEN %s
        #                   WHEN "runner_book"."rating" = %s THEN %s ELSE %s END) AS "pub1"
        #   FROM "runner_book"
        #   WHERE "runner_book"."rating" > %s
        #   GROUP BY "runner_book"."rating"
        #   LIMIT 21' - PARAMS = (5.0, 0, 4.0, 1, 0, 5.0, 1, 4.0, 0, 0, 3.0)

        print(b)
        dump_sql()

