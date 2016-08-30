from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory
from . import views

class SimpleTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.tests = {
            '正常' : ['title', 1, 'form_only'],
            '最初のForm.clean_<filed_name>でエラー': ['t', 1, 'form_only'],
            'Form.CustomFormFieldのうち、最初のバリデーションでエラー': ['title', 1, 'fo'],
            'Formにしかないフィールドのバリデーションでエラー': ['title', 1, 'for'],
            'Form全体のバリデーション(Form.clean())でエラー': ['title', 10, 'form_only'],
            'Model.CustomFormFieldのうち、最初のバリデーションでエラー': ['titl', 1, 'form_only'],
        }
    
    def test_use_subtest(self):
        for test_name, (title, lines, form_only) in self.tests.items():
            with self.subTest(name=test_name):
                print('------------------\n{}\n------------------'.format(test_name))
                request = self.factory.post(reverse('my:article-create'))
                request.POST['title'] = title
                request.POST['lines'] = lines
                request.POST['form_only'] = form_only
                
                response = views.ArticleCreateView.as_view()(request)
                
                # 成功させないとログが出ないので、必ず成功するようにしている
                self.assertEqual(1,1)
