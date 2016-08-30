from django.core.management.base import BaseCommand
from libs.dump import dump_sql
from apps.runner.models import Book, Publisher, Author

class Command(BaseCommand):
    # manage.pyで動作させた時に引数を受け取れるようにする
    args = '引数'

    def handle(self, *args, **options):

        if 'inner' in args:
            self.inner_join()

        if 'left' in args:
            self.left_join()

        if 'backward' in args:
            self.backward_join()

        if 'multi' in args:
            self.multi_join()


    def inner_join(self):
        # 微妙に違うSQLが出される

        # INNER JOINするけど、SELECT句にはpublisherの列は無い
        b1 = Book.objects.filter(publisher__num_awards=5).values()
        #=> SELECT "runner_book"."id", "runner_book"."name", "runner_book"."pages", "runner_book"."price",
        #          "runner_book"."rating", "runner_book"."publisher_id", "runner_book"."pubdate"
        #   FROM "runner_book"
        #   INNER JOIN "runner_publisher" ON ( "runner_book"."publisher_id" = "runner_publisher"."id" )
        #   WHERE "runner_publisher"."num_awards" = %s
        #   LIMIT 21 - PARAMS = (5,)

        print(b1)
        dump_sql()

        # INNER JOINし、SELECT句にもpublisherの列がある
        b2 = Book.objects.select_related().all().values()
        #=> SELECT "runner_book"."id", "runner_book"."name", "runner_book"."pages", "runner_book"."price",
        #          "runner_book"."rating", "runner_book"."publisher_id", "runner_book"."pubdate",
        #          "runner_publisher"."id", "runner_publisher"."name", "runner_publisher"."num_awards"
        #   FROM "runner_book"
        #   INNER JOIN "runner_publisher" ON ( "runner_book"."publisher_id" = "runner_publisher"."id" )
        #   LIMIT 21 - PARAMS = ()

        print(b2)
        dump_sql()

        # INNER JOINとWHEREを使って、全列出す
        b3 = Book.objects.filter(publisher__num_awards=5).select_related().all().values()
        #=> SELECT "runner_book"."id", "runner_book"."name", "runner_book"."pages", "runner_book"."price",
        #          "runner_book"."rating", "runner_book"."publisher_id", "runner_book"."pubdate",
        #          "runner_publisher"."id", "runner_publisher"."name", "runner_publisher"."num_awards"
        #   FROM "runner_book"
        #   INNER JOIN "runner_publisher" ON ( "runner_book"."publisher_id" = "runner_publisher"."id" )
        #   WHERE "runner_publisher"."num_awards" = %s
        #   LIMIT 21 - PARAMS = (5,)

        print(b3)
        dump_sql()


    def left_join(self):
        # id IS NULL
        # p1 = Publisher.objects.filter(book__isnull=False)  # これだと、INNER JOIN になる

        p1 = Publisher.objects.filter(book__isnull=True).values()
        #=> SELECT *
        #   FROM "runner_publisher"
        #   LEFT OUTER JOIN "runner_book" ON ( "runner_publisher"."id" = "runner_book"."publisher_id" )
        #   WHERE "runner_book"."id" IS NULL

        print(p1)
        dump_sql()

        # publisher_id IS NULL
        p2 = Publisher.objects.filter(book__publisher__isnull=True).values()
        #=> SELECT *
        #   FROM "runner_publisher"
        #   LEFT OUTER JOIN "runner_book" ON ( "runner_publisher"."id" = "runner_book"."publisher_id" )
        #   WHERE "runner_book"."publisher_id" IS NULL

        print(p2)
        dump_sql()


    def backward_join(self):
        # p = Author.objects.filter(age__gt=5)や
        # p = Author.objects.all() だと逆引きできない

        a = Author.objects.get(pk=1).book_set.all().values()
        #=> SELECT "runner_book"."id", "runner_book"."name", "runner_book"."pages", "runner_book"."price",
        #          "runner_book"."rating", "runner_book"."publisher_id", "runner_book"."pubdate"
        #   FROM "runner_book"
        #   INNER JOIN "runner_book_authors" ON ( "runner_book"."id" = "runner_book_authors"."book_id" )
        #   WHERE "runner_book_authors"."author_id" = %s
        #   LIMIT 21 - PARAMS = (1,)

        print(a)
        dump_sql()


    def multi_join(self):
        a = Author.objects.filter(book__publisher__name='Pub2').values()
        #=> SELECT "runner_author"."id", "runner_author"."name", "runner_author"."age"
        #   FROM "runner_author"
        #   INNER JOIN "runner_book_authors" ON ( "runner_author"."id" = "runner_book_authors"."author_id" )
        #       INNER JOIN "runner_book" ON ( "runner_book_authors"."book_id" = "runner_book"."id" )
        #           INNER JOIN "runner_publisher" ON ( "runner_book"."publisher_id" = "runner_publisher"."id" )
        #   WHERE "runner_publisher"."name" = %s
        #   LIMIT 21 - PARAMS = ('Pub2',)

        print(a)
        dump_sql()