from django.core.management.base import BaseCommand
from libs.dump import dump_sql, dump_pk
from apps.runner.models import Book

class Command(BaseCommand):
    # manage.pyで動作させた時に引数を受け取れるようにする
    args = '引数'

    def handle(self, *args, **options):
        # 比較のため、全件を出力しておく
        b = Book.objects.all()
        dump_pk(b)
        print('--------------')

        if 'only' in args:
            self.limit_only()

        if 'offset' in args:
            self.limit_offset()

        if 'offset_step' in args:
            self.limit_offset_step()


    def limit_only(self):
        b = Book.objects.all()[:2]
        #=> SELECT * FROM "runner_book" LIMIT 2

        dump_pk(b)
        dump_sql()


    def limit_offset(self):
        # 2-3番目を取り出す
        b = Book.objects.all()[1:3]
        #=> SELECT * FROM "runner_book" LIMIT 2 OFFSET 1

        dump_pk(b)
        dump_sql()


    def limit_offset_step(self):
        # 始まり1、終わり3、step2
        b = Book.objects.all()[:3:2]
        #=> SELECT * FROM "runner_book" LIMIT 3

        dump_pk(b)
        dump_sql()

