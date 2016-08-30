from django.db import models
from django.core.exceptions import ValidationError
from .utils import print_with_indent

def dummy_validator_for_custom_field(value):
    '''Articleのtitleフィールドで指定するvalidators用'''
    print_with_indent('Model.custom_field.validator', 7)
    
def dummy_validator_for_lines(value):
    '''Articleのlineフィールドで指定するvalidators用'''
    print_with_indent('Model.lines.validator', 6)

class CustomModelField(models.CharField):
    '''Articleのtitleフィールド用'''
    def to_python(self, value):
        print_with_indent('Model.custom_field.to_python()', 7)
        
        if len(value) == 4:
            # 挙動を確認するためのバリデーション
            raise ValidationError('CustomModelField.to_pythonで長さ4文字はダメ')
        return super(CustomModelField, self).to_python(value)
    
    def validate(self, value, model_instance):
        print_with_indent('Model.custom_field.validate()', 7)
        return super(CustomModelField, self).validate(value, model_instance)
        
    def clean(self, value, model_instance):
        print_with_indent('Model.custom_field.clean()', 6)
        return super(CustomModelField, self).clean(value, model_instance)


class Article(models.Model):
    title = CustomModelField('Title', max_length=255, 
                             validators=[dummy_validator_for_custom_field])
    lines = models.DecimalField('Lines', max_digits=10, decimal_places=0,
                                validators=[dummy_validator_for_lines])
        
    def full_clean(self, exclude=None, validate_unique=True):
        print_with_indent('Model.full_clean()', 4)
        return super(Article, self).full_clean(exclude, validate_unique)
        
    def clean_fields(self, exclude=None):
        print_with_indent('Model.clean_fields()', 5)
        return super(Article, self).clean_fields(exclude)
        
    def clean(self):
        print_with_indent('Model.clean()', 5)
        return super(Article, self).clean()
        
    def validate_unique(self, exclude=None):
        print_with_indent('Model.validate_unique()', 5)
        return super(Article, self).validate_unique(exclude)
        
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        print_with_indent('Model.save()', 2)
        return super(Article, self).save(force_insert, force_update, using, update_fields)
