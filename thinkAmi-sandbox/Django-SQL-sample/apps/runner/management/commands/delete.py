from django.core.management.base import BaseCommand
from apps.runner.models import *
from libs.dump import dump_sql
import traceback


def initialize():
    '''関係するテーブルの初期化'''
    CascadeKey.objects.get_or_create(name='cascade')
    ProtectKey.objects.get_or_create(name='protect')
    SetNullKey.objects.get_or_create(name='set_null')
    SetDefaultKey.objects.get_or_create(name='set_default')
    SetDefaultKey.objects.create(name='on_default')
    SetKey.objects.get_or_create(name='set_row')
    DoNothingKey.objects.get_or_create(name='do_nothing')

    Deletion.objects.get_or_create(
        name = 'foo',
        cascade_row = CascadeKey.objects.get(name='cascade'),
        protect_row = ProtectKey.objects.get(name='protect'),
        set_null_row = SetNullKey.objects.get(name='set_null'),
        set_default_row = SetDefaultKey.objects.get(name='set_default'),
        set_key_row = SetKey.objects.get(name='set_row'),
        do_nothing_row = DoNothingKey.objects.get(name='do_nothing'),
    )


def dump_related_models(model):
    print('related_model: {0}'.format(model.objects.all().values()))
    print('Deletion_model: {0}'.format(Deletion.objects.all().values()))

class Command(BaseCommand):
    args = '引数'

    def handle(self, *args, **options):
        initialize()

        if 'all' in args:
            self.delete_all()

        if 'filter' in args:
            self.delete_filter()

        if 'cascade' in args:
            self.delete_cascade()

        if 'protect' in args:
            self.delete_protect()

        if 'null' in args:
            self.delete_set_null()

        if 'default' in args:
            self.delete_set_default()

        if 'set' in args:
            self.delete_set()

        if 'nothing' in args:
            self.delete_nothing()


    def delete_all(self):
        '''全件削除'''
        Deletion.objects.all().delete()
        dump_sql()
        #=> DELETE FROM "runner_deletion"

        print(Deletion.objects.all().values()) #=> []


    def delete_filter(self):
        '''条件一致のみ削除'''
        Deletion.objects.filter(name='foo').delete()
        dump_sql()
        #=> 'DELETE FROM "runner_deletion" WHERE "runner_deletion"."name" = %s' - PARAMS = ('foo',)

        print(Deletion.objects.all().values()) #=> []


    def delete_cascade(self):
        '''cascadeな削除'''
        dump_related_models(CascadeKey)
        #=> related_model: [{'name': 'cascade', 'id': 3}]
        #   Deletion_model: [{'cascade_row_id': 3, 'name': 'foo', 'id': 5}]  *関係する部分のみ

        CascadeKey.objects.all().delete()
        dump_sql()
        #=> 'DELETE FROM "runner_cascadekey" WHERE "runner_cascadekey"."id" IN (%s)' - PARAMS = (1,)


        dump_related_models(CascadeKey)
        #=> related_model: []
        #   Deletion_model: []


    def delete_protect(self):
        '''protectな削除'''
        dump_related_models(ProtectKey)
        #=> related_model: [{'id': 1, 'name': 'protect'}]
        #   Deletion_model: [{'id': 6, 'protect_row_id': 1, 'name': 'foo'}]

        try:
            # 削除しようとしたらエラーを吐く
            ProtectKey.objects.all().delete()
            dump_related_models(ProtectKey) #=> ここまで到達しない

        except:
            print('-------')
            # django.db.models.deletion.ProtectedError: ("Cannot delete some instances of model 'ProtectKey'
            # because they are referenced through a protected foreign key:
            # 'DeleteOn.protect_row'", [<DeleteOn: DeleteOn object>])
            traceback.print_exc()


    def delete_set_null(self):
        '''nullをセットする削除'''
        dump_related_models(SetNullKey)
        #=> related_model: [{'id': 1, 'name': 'set_null'}]
        #   Deletion_model: [{'name': 'foo', 'id': 6, 'set_null_row_id': 1}]

        SetNullKey.objects.all().delete()
        dump_sql()
        #=> 'DELETE FROM "runner_setnullkey" WHERE "runner_setnullkey"."id" IN (%s)' - PARAMS = (1,)

        dump_related_models(SetNullKey)
        #=> related_model: []
        #   Deletion_model: [{'name': 'foo', 'id': 6, 'set_null_row_id': None}]


    def delete_set_default(self):
        '''Deletionのdefault値をセットする削除'''
        dump_related_models(SetDefaultKey)
        #=> related_model: [{'name': 'set_default', 'id': 11}, {'name': 'on_default', 'id': 12}]
        #   Deletion_model: [{'id': 8, 'name': 'foo', 'set_default_row_id': 11}]

        SetDefaultKey.objects.filter(name='set_default').delete()
        dump_sql()
        #=> 'DELETE FROM "runner_setdefaultkey" WHERE "runner_setdefaultkey"."id" IN (%s)' - PARAMS = (11,)

        dump_related_models(SetDefaultKey)
        #=> related_model: [{'name': 'on_default', 'id': 12}]
        #   Deletion_model: [{'id': 8, 'name': 'foo', 'set_default_row_id': 9}]


    def delete_set(self):
        '''on_deleteで設定したSETの結果をセットする削除'''
        dump_related_models(SetKey)
        #=> related_model: [{'id': 3, 'name': 'set_row'}]
        #   Deletion_model: [{'id': 9, 'name': 'foo', 'set_key_row_id': 3}]

        SetKey.objects.filter(name='set_row').delete()
        dump_sql()
        #=> 'DELETE FROM "runner_setkey" WHERE "runner_setkey"."id" IN (%s)' - PARAMS = (3,)

        dump_related_models(SetKey)
        #=> related_model: []
        #   Deletion_model: [{'id': 9, 'name': 'foo', 'set_key_row_id': 11}]


    def delete_nothing(self):
        '''何も値を変更しない削除'''
        dump_related_models(DoNothingKey)
        #=> related_model: [{'id': 4, 'name': 'do_nothing'}]
        #   Deletion_model: [{'do_nothing_row_id': 4, 'id': 11, 'name': 'foo'}]

        DoNothingKey.objects.filter(name='do_nothing').delete()
        dump_sql()
        #=> 'DELETE FROM "runner_donothingkey" WHERE "runner_donothingkey"."name" = %s' - PARAMS = ('do_nothing',)

        dump_related_models(DoNothingKey)
        #=> related_model: []
        #   Deletion_model: [{'do_nothing_row_id': 4, 'id': 11, 'name': 'foo'}]
