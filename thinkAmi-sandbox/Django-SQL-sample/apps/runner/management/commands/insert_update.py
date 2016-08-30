from django.core.management.base import BaseCommand
from django.db.models import F
from django.db import transaction
from libs.dump import dump_sql_postgres, dump_pk
from apps.runner.models import Store


def dump_store():
    '''Store modelのダンプ'''
    [print(s) for s in Store.objects.all().values()]


class Command(BaseCommand):
    args = '引数'

    def handle(self, *args, **options):
        if 'insert' in args:
            self.insert()

        if 'update_one' in args:
            self.update_record()

        if 'update_multi' in args:
            self.update_records()

        if 'get_or_create' in args:
            self.get_or_create()

        if 'update_or_create' in args:
            self.update_or_create()

        if 'update_field' in args:
            self.update_field()

        if 'select_for_update' in args:
            self.select_for_update()


    def insert(self):
        '''INSERT'''

        # メソッドチェーンでのINSERT
        Store(name='st1', registered_users=1).save()
        dump_sql_postgres()
        #=> INSERT INTO "store" ("name", "registered_users", "hoge") VALUES ('st1', 1, 'fuga') RETURNING "store"."id"

        # primary keyの確認のために、分割
        s = Store(name='st2', registered_users=2)
        dump_pk(s) #=> None
        s.save()
        dump_pk(s) #=> pk:2


    def update_record(self):
        '''1レコードのUPDATE'''

        # UPDATE元のデータ作成
        self.insert()
        dump_store() #=> {'registered_users': 1, 'hoge': 'fuga', 'name': 'st1', 'id': 1}

        # 繰り返すと複数件取れてしまうので、1件のみに絞る
        s = Store.objects.filter(name='st1').first()
        s.registered_users += 1
        s.save()
        dump_sql_postgres()
        #=> UPDATE "store" SET "name" = 'st1', "registered_users" = 2, "hoge" = 'fuga' WHERE "store"."id" = 1

        dump_store() #=> {'registered_users': 2, 'hoge': 'fuga', 'name': 'st1', 'id': 1}


    def update_records(self):
        '''複数レコードのUPDATE'''

        # UPDATE元のデータ作成
        self.insert()
        dump_store()
        #=> {'hoge': 'fuga', 'id': 1, 'registered_users': 2, 'name': 'st1'}
        #   {'hoge': 'fuga', 'id': 2, 'registered_users': 2, 'name': 'st2'}

        # Fオブジェクトを使って、複数行のregistered_users列をインクリメント
        Store.objects.values().filter(name__istartswith='st').update(registered_users=F('registered_users') + 1)
        dump_sql_postgres()
        #=> UPDATE "store" SET "registered_users" = ("store"."registered_users" + 1)
        #    WHERE UPPER("store"."name"::text) LIKE UPPER('st%')

        dump_store()
        #=> {'hoge': 'fuga', 'id': 1, 'registered_users': 3, 'name': 'st1'}
        #   {'hoge': 'fuga', 'id': 2, 'registered_users': 3, 'name': 'st2'}


    def get_or_create(self):
        '''get_or_createでレコードが作成されるタイミング'''

        # 実行前に全削除
        Store.objects.all().delete()
        print(Store.objects.count())

        # created=True
        s1, c1 = Store.objects.get_or_create(
            name = 'get_or_create1',
            registered_users = 2,
            hoge = 'fuga1',
        )
        print(s1)
        print(c1)
        dump_sql_postgres()
        #=> NSERT INTO "store" ("name", "registered_users", "hoge") VALUES ('get_or_create1', 2, 'fuga1')

        # created=False
        s2, c2 = Store.objects.get_or_create(
            name = 'get_or_create1',
            registered_users = 2,
        )
        print(s2)
        print(c2)
        dump_sql_postgres()
        #=> SELECT * FROM "store" WHERE ("store"."registered_users" = 2 AND "store"."name" = 'get_or_create1')

        # created=False
        s3, c3 = Store.objects.get_or_create(
            name = 'get_or_create1',
        )
        print(s3)
        print(c3)

        # created=False
        s4, c4 = Store.objects.get_or_create(
            registered_users = 2,
        )
        print(s4)
        print(c4)

        # created=True
        s5, c5 = Store.objects.get_or_create(
            name = 'get_or_create2',
            registered_users = 2,
        )
        print(s5)
        print(c5)

        # 複数件取れてしまうため、例外が出る
        # apps.runner.models.MultipleObjectsReturned: get() returned more than one Stores -- it returned 2!
        s6, c6 = Store.objects.get_or_create(
            registered_users = 2,
        )
        print(s6)
        print(c6)


    def update_or_create(self):
        '''update_or_createでレコードが作成されるタイミング'''

        # 実行前に全削除
        Store.objects.all().delete()
        print(Store.objects.count())

        # created=True
        s1, c1 = Store.objects.update_or_create(
            name = 'update_or_create1',
            registered_users = 2,
            hoge = 'fuga1',
        )
        print(s1)
        print(c1)
        dump_sql_postgres()
        #=> NSERT INTO "store" ("name", "registered_users", "hoge") VALUES ('update_or_create1', 2, 'fuga1')

        # created=False
        s2, c2 = Store.objects.update_or_create(
            name = 'update_or_create1',
            registered_users = 2,
        )
        print(s2)
        print(c2)
        dump_sql_postgres()
        #=> UPDATE "store" SET "name" = 'update_or_create1', "registered_users" = 2, "hoge" = 'fuga1'
        #    WHERE "store"."id" = 17

        # created=False
        s3, c3 = Store.objects.update_or_create(
            name = 'update_or_create1',
        )
        print(s3)
        print(c3)

        # created=False
        s4, c4 = Store.objects.update_or_create(
            registered_users = 2,
        )
        print(s4)
        print(c4)

        # created=True
        s5, c5 = Store.objects.update_or_create(
            name = 'update_or_create2',
            registered_users = 2,
        )
        print(s5)
        print(c5)

        # 複数件取れてしまうため、例外が出る
        # apps.runner.models.MultipleObjectsReturned: get() returned more than one Stores -- it returned 2!
        s6, c6 = Store.objects.update_or_create(
            registered_users = 2,
        )
        print(s6)
        print(c6)


    def update_field(self):
        '''update_or_createを使った列の更新'''

        # 実行前に全削除
        Store.objects.all().delete()
        print(Store.objects.count())

        # データ登録
        s1, c1 = Store.objects.update_or_create(
            name = 'update_or_create1',
            hoge = 'fuga1',
            registered_users = 1,
        )
        dump_sql_postgres()
        #=> INSERT INTO "store" ("name", "registered_users", "hoge") VALUES ('update_or_create1', 1, 'fuga1')
        print(c1)    #=> True
        dump_store() #=> {'hoge': 'fuga1', 'registered_users': 1, 'id': 20, 'name': 'update_or_create1'}

        # defaultsで指定した列・値で更新する
        s2, c2 = Store.objects.update_or_create(
            name = 'update_or_create1',
            hoge = 'fuga1',
            defaults={
                'hoge': 'fuga2'
            }
        )
        dump_sql_postgres()
        #=> PDATE "store" SET "name" = 'update_or_create1', "registered_users" = 1, "hoge" = 'fuga2'
        #   WHERE "store"."id" = 20
        print(c2)    #=> False
        dump_store() #=> {'hoge': 'fuga2', 'registered_users': 1, 'id': 20, 'name': 'update_or_create1'}


    def select_for_update(self):
        '''SELECT FOR UPDATE'''

        # トランザクション外だとエラーになる
        # django.db.transaction.TransactionManagementError: select_for_update cannot be used outside of a transaction.
        # PostgreSQLの場合
        with transaction.atomic(using='postgres'):
            repr(Store.objects.select_for_update().filter(name='st1')) # reprで即時評価
            dump_sql_postgres()
            #=> SELECT * FROM "store" WHERE "store"."name" = 'st1' LIMIT 21 FOR UPDATE

        # SQLiteの場合、SELECT FOR UPDATEに対応していないため、
        # エラーが出ずに`FOR UPDATE`なしのSQLが発行される