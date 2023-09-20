from django.urls import path
from pioner_gallery import views
from django.urls import path
from pioner_gallery.blog.views import ArticlesListView

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('cover_page', views.cover_page, name='cover_page'),
    path('contact_page', views.contact_page, name='contact_page'),
    path('gallery', views.gallery, name='gallery'),
    path('blog', views.blog, name='blog'),
    path('marketplace', views.marketplace, name='marketplace'),
    path('', ArticlesListView.as_view(), name='articles_list'),
]
