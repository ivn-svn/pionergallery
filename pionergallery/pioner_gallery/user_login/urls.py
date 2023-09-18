from django.contrib import admin
from django.urls import path, include
from pioner_gallery import views

urlpatterns = [
    path('user_login/', views.user_login, name='user_login'),
    path('register/', views.register_view, name='register'),
    path('delete_user_profile/', views.delete_user_profile, name='delete_user_profile'),
    path('delete_confirmation/', views.delete_confirmation, name='delete_confirmation'),
]
