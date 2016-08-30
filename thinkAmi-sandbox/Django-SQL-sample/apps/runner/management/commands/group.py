from django.core.management.base import BaseCommand
from django.db.models import Avg, Sum, Max
from libs.dump import dump_sql
from apps.runner.models import Book

class Command(BaseCommand):
    # manage.pyで動作させた時に引数を受け取れるようにする
    args = '引数'

    def handle(self, *args, **options):
        if 'all_avg' in args:
            self.all_avg()

        if 'all_sum' in args:
            self.all_sum()

        if 'avg' in args:
            self.avg()

        if 'sum' in args:
            self.extra_sum()

        if 'max' in args:
            self.extra_max()


    def all_avg(self):
        # 集計結果には明示的な名前を付けない
        b = Book.objects.all().aggregate(Avg('price'))
        #=> SELECT AVG("runner_book"."price") AS "price__avg" FROM "runner_book"

        print(b)
        dump_sql()


    def all_sum(self):
        # 集計結果に対し、明示的に名前をつける
        b = Book.objects.all().aggregate(sum_price=Sum('price'))
        #=> SELECT SUM("runner_book"."price") AS "sum_price" FROM "runner_book"

        print(b)
        dump_sql()


    def avg(self):
        # ポイント:
        # 　・`GROUP BY`する場合、values.annotate の順で書く
        # 　・集約キーはvalues内に書く
        # 　・annotateで新しい集約列を追加
        # `GROUP BY`されない例
        # 　books = Book.objects.annotate(price_avg=Avg('price')).values('publisher_id')

        b = Book.objects.all().values('publisher_id').annotate(price_avg=Avg('price'))
        #=> SELECT "runner_book"."publisher_id", AVG("runner_book"."price") AS "price_avg"
        #   FROM "runner_book"
        #   GROUP BY "runner_book"."publisher_id"

        print(b)
        dump_sql()


    def extra_sum(self):
        # SQLiteの関数`strftime`を使うために、extraを使った例
        b = Book.objects.all()\
                    .extra(select={'month': "strftime('%m', pubdate)"})\
                    .values('month')\
                    .annotate(sum_price=Sum('price'))
        #=> SELECT (strftime(\'%m\', pubdate)) AS "month", SUM("runner_book"."price") AS "sum_price"
        #   FROM "runner_book"
        #   GROUP BY (strftime(\'%m\', pubdate))

        print(b)
        dump_sql()


    def extra_max(self):
        # SQLiteの関数`strftime`を使うために、extraを使った例
        # monthの値をstringからintにキャスト
        b = Book.objects.all()\
                    .extra(select={'month': "cast(strftime('%m', pubdate) AS integer)"})\
                    .values('month')\
                    .annotate(max_price=Max('price'))
        #=> SELECT (cast(strftime(\'%m\', pubdate) AS integer)) AS "month", MAX("runner_book"."price") AS "max_price"
        #   FROM "runner_book"
        #   GROUP BY (cast(strftime(\'%m\', pubdate) AS integer))

        print(b)
        dump_sql()