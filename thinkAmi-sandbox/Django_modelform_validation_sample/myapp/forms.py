from django import forms
from .models import Article
from .utils import print_with_indent

def dummy_validator_for_custom_field(value):
    '''ArticleFormのform_onlyフィールドで指定するvalidators用'''
    print_with_indent('Form.custom_field.validator', 5)
    
class CustomFormField(forms.CharField):
    '''ArticleFormのform_onlyフィールド用'''
    def to_python(self, value):
        print_with_indent('Form.custom_field.to_python()', 5)
        
        if len(value) == 2:
            # 挙動を確認するためのバリデーション
            raise forms.ValidationError('CustomFormField.to_pythonで長さ2文字はダメ')
        return super(CustomFormField, self).to_python(value)
    
    def validate(self, value):
        print_with_indent('Form.custom_field.validate()', 5)
        return super(CustomFormField, self).validate(value)
        
    def clean(self, value):
        print_with_indent('Form.custom_field.clean()', 4)
        return super(CustomFormField, self).clean(value)
        

class ArticleForm(forms.ModelForm):
    form_only = CustomFormField(required=False,
                                validators=[dummy_validator_for_custom_field])
                                
    def is_valid(self):
        print_with_indent('Form.is_valid()', 0)
        return super(ArticleForm, self).is_valid()
        
    def full_clean(self):
        print_with_indent('Form.full_clean()', 2)
        return super(ArticleForm, self).full_clean()
        
    def _clean_fields(self):
        print_with_indent('Form._clean_fields()', 3)
        return super(ArticleForm, self)._clean_fields()
        
    def _clean_form(self):
        print_with_indent('Form._clean_form()', 3)
        return super(ArticleForm, self)._clean_form()
        
    def _post_clean(self):
        print_with_indent('Form._post_clean()', 3)
        return super(ArticleForm, self)._post_clean()
        
    def clean(self):
        print_with_indent('Form.clean()', 4)
        # ModelFormでオーバーライドして、unique系のバリデーション結果を残すには、親クラスのclean()を呼ぶこと
        # https://docs.djangoproject.com/en/1.9/topics/forms/modelforms/#overriding-the-clean-method
        cleaned_data = super(ArticleForm, self).clean()
        if cleaned_data.get('lines') == 10:
            # 挙動を確認するためのバリデーション
            # "title"や"form_only"だと、
            # ここに至るまでのバリデーションエラーが原因で
            # cleaned_dataに設定されていない可能性があるため、
            # 他のバリデーションで使っていない"lines"にて判定する
            raise forms.ValidationError('Form.clean()でlinesが10だとダメ')
        return cleaned_data
        
    def clean_title(self):
        print_with_indent('Form.clean_title()', 4)
        title = self.cleaned_data['title']
        if len(title) == 1:
            raise forms.ValidationError('clean_titleで長さ1文字はダメ')
        return title
        
    def clean_lines(self):
        print_with_indent('Form.clean_lines()', 4)
        return self.cleaned_data['lines']
        
    def clean_form_only(self):
        print_with_indent('Form.clean_form_only()', 4)
        form_only = self.cleaned_data['form_only']
        if len(form_only) == 3:
            # 挙動を確認するためのバリデーション
            raise forms.ValidationError('clean_form_onlyで長さ3文字はダメ')
        return form_only
    
    @property
    def errors(self):
        print_with_indent('Form.errors', 1)
        return super(ArticleForm, self).errors
        
    def save(self, commit=True):
        print_with_indent('Form.save()', 0)
        return super(ArticleForm, self).save()
        
    class Meta:
        model = Article
        fields = '__all__'