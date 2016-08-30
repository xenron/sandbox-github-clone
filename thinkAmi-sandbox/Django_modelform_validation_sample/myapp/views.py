from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse

from .forms import ArticleForm
from .models import Article

class ArticleCreateView(CreateView):
    model = Article
    form_class = ArticleForm
    
    def get_success_url(self):
        return reverse('my:article-detail', args=(self.object.id,))
        