from django.db import connection, connections
import collections

def dump_sql():
    '''SQL文をprintする'''
    for sql in map((lambda r: r['sql']), connection.queries[-1:]):
        print(sql)

def dump_sql_postgres():
    '''SQL文をprintする'''
    for sql in map((lambda r: r['sql']), connections['postgres'].queries[-1:]):
        print(sql)

def dump_pk(model):
    '''modelのpkを表示する'''
    if isinstance(model, collections.Iterable):
        [print('pk:{0.pk}'.format(x)) for x in model]
    else:
        print('pk:{0.pk}'.format(model))