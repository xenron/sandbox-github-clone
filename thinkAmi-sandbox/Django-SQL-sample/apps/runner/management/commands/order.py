from django.core.management.base import BaseCommand
from libs.dump import dump_sql
from apps.runner.models import Book

class Command(BaseCommand):
    # manage.pyで動作させた時に引数を受け取れるようにする
    args = '引数'

    def handle(self, *args, **options):
        if 'asc' in args:
            self.order_by_asc()

        if 'desc' in args:
            self.order_by_desc()


    def order_by_asc(self):
        b = Book.objects.all().order_by('pages').values()
        #=> SELECT * FROM "runner_book" ORDER BY "runner_book"."pages" ASC - PARAMS = ()

        print(b)
        dump_sql()


    def order_by_desc(self):
        b = Book.objects.all().order_by('-pages').values()
        #=> SELECT * FROM "runner_book" ORDER BY "runner_book"."pages" DESC - PARAMS = ()

        print(b)
        dump_sql()

