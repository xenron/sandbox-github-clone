from django.conf.urls import url
from django.views.generic import DetailView
from . import views, models

urlpatterns = [
    url(r'^create/$', views.ArticleCreateView.as_view(), name='article-create'),
    url(r'^(?P<pk>[0-9]+)/$', DetailView.as_view(model=models.Article), name='article-detail'),
]