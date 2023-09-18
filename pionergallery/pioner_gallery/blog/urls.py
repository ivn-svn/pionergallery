from django.urls import path
from pioner_gallery import views
from django.urls import path

from pioner_gallery.blog.views import list_articles, ArticlesListView, ArticleDetailView \
    , ArticleCreateView, ArticleDeleteView

urlpatterns = [
    path('page_list/', views.blog, name='page_list'),
    path('list_articles_blog/', ArticlesListView.as_view(), name='list_articles_blog'),
    path('blog/<int:pk>/', ArticleDetailView.as_view(), name='details_article'),
    path('cbv/create/', ArticleCreateView.as_view(), name='create_article'),
    path('cbv/delete/<int:pk>/', ArticleDeleteView.as_view(), name='delete_article'),
    #   path('redirect-to-articles/', RedirectToArticlesView.as_view(), name='redirect_to_articles'),
]
