from django.core.management.base import BaseCommand
from libs.dump import dump_sql
from apps.runner.models import Book

class Command(BaseCommand):
    # manage.pyで動作させた時に引数を受け取れるようにする
    args = '引数'

    def handle(self, *args, **options):
        if 'all' in args:
            self.select_all()

        if 'part' in args:
            self.select_particular_column()


    def select_all(self):
        b = Book.objects.all().values()
        #=> 'SELECT * FROM "runner_book"'
        # 注) 実際は列名が全部列挙されるけど、スペースの関係上`*`で表記

        print(b)
        dump_sql()


    def select_particular_column(self):
        b = Book.objects.all().values('name')
        #=> SELECT "runner_book"."name" FROM "runner_book"

        print(b)
        dump_sql()