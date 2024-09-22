from django.urls import path

from blog.apps import BlogConfig
from blog.views import ArticleListView, ArticleDetailView, ArticleCreateView

app_name = BlogConfig.name

urlpatterns = [
    path('', ArticleListView.as_view(), name='article_list'),
    path("view/<int:pk>", ArticleDetailView.as_view(), name="article_detail"),
    path("create/", ArticleCreateView.as_view(), name="create_article"),
]