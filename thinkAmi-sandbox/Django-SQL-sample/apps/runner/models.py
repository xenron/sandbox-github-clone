from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()

class Publisher(models.Model):
    name = models.CharField(max_length=300)
    num_awards = models.IntegerField()

class Book(models.Model):
    name = models.CharField(max_length=300)
    pages = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.FloatField()
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher)
    pubdate = models.DateField()

class Store(models.Model):
    name = models.CharField(max_length=300)
    registered_users = models.PositiveIntegerField()
    hoge = models.CharField(max_length=100, default='fuga')

    class Meta:
        db_table = 'store'

class CascadeKey(models.Model):
    name = models.CharField(max_length=100)

class ProtectKey(models.Model):
    name = models.CharField(max_length=100)

class SetNullKey(models.Model):
    name = models.CharField(max_length=100)

class SetDefaultKey(models.Model):
    name = models.CharField(max_length=100)

class SetKey(models.Model):
    name = models.CharField(max_length=100)

class DoNothingKey(models.Model):
    name = models.CharField(max_length=100)

class Deletion(models.Model):
    name = models.CharField(max_length=200)
    cascade_row = models.ForeignKey(CascadeKey, on_delete=models.CASCADE)
    protect_row = models.ForeignKey(ProtectKey, on_delete=models.PROTECT)
    set_null_row = models.ForeignKey(SetNullKey,
                                     null=True,
                                     on_delete=models.SET_NULL)
    set_default_row = models.ForeignKey(SetDefaultKey,
                                        default=9,
                                        on_delete=models.SET_DEFAULT)
    set_key_row = models.ForeignKey(SetKey,
                                    default=10,
                                    on_delete=models.SET(11))
    do_nothing_row = models.ForeignKey(DoNothingKey, on_delete=models.DO_NOTHING)