class DatabaseRouter(object):
    def db_for_read(self, model, **hints):
        # 通常はapp_labelを使うと思われるが、
        # 今回は同じアプリ内なので、識別する方法として`db_table`を使う
        if model._meta.db_table == 'store':
            # DATABASESのconnection名を返す
            # テーブル名ではないので注意
            return 'postgres'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.db_table == 'store':
            return 'postgres'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        # 今回のアプリではJOINは扱わないので、デフォルトのNoneを返す
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # Migrationは常に許可する
        return True
