from django.core.management.base import BaseCommand
from django.db.models import Q
from libs.dump import dump_sql
from apps.runner.models import Book

class Command(BaseCommand):
    # manage.pyで動作させた時に引数を受け取れるようにする
    args = '引数'

    def handle(self, *args, **options):
        if 'eq' in args:
            self.where_equal()

        if 'not' in args:
            self.where_not_equal()

        if 'and' in args:
            self.where_and()

        if 'or' in args:
            self.where_or()

        if 'contain' in args:
            self.where_contain()


    def where_equal(self):
        b = Book.objects.all().filter(pubdate='2015-10-01').values()
        #=> 'SELECT * FROM "runner_book" WHERE "runner_book"."pubdate" = %s' - PARAMS = ('2015-10-01',)

        print(b)
        dump_sql()


    def where_not_equal(self):
        b = Book.objects.all().exclude(pubdate='2015-10-01').values()
        #=> 'SELECT * FROM "runner_book" WHERE NOT ("runner_book"."pubdate" = %s)' - PARAMS = ('2015-10-01',)]

        print(b)
        dump_sql()


    def where_and(self):
        b = Book.objects.all().filter(pubdate='2015-10-01', publisher=1).values()
        #=> 'SELECT * FROM "runner_book"
        #    WHERE ("runner_book"."publisher_id" = %s AND "runner_book"."pubdate" = %s)' - PARAMS = (1, '2015-10-01')

        print(b)
        dump_sql()


    def where_or(self):
        b = Book.objects.all().filter(Q(pubdate='2015-10-01') | Q(publisher=1)).values()
        #=> 'SELECT * FROM "runner_book"
        #    WHERE ("runner_book"."pubdate" = %s OR "runner_book"."publisher_id" = %s)' - PARAMS = ('2015-10-01', 1)

        print(b)
        dump_sql()


    def where_contain(self):
        b = Book.objects.all().filter(name__contains='d').values()
        #=> 'SELECT * FROM "runner_book" WHERE "runner_book"."name" LIKE %s ESCAPE \'\\\'' - PARAMS = ('%d%',)

        print(b)
        dump_sql()