"""
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from . import views
from pioner_gallery.marketplace import views as marketplaceviews
from django.conf.urls import handler404
from .views import Custom404View, Custom500View

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pioner_gallery.webapp.urls')),
    path('', include('pioner_gallery.blog.urls')),
    path('', include('pioner_gallery.marketplace.urls')),
    path('', include('pioner_gallery.user_login.urls')),
    path('', include('pioner_gallery.mediaplanner.urls')),
    path('user_logout/', views.UserLogoutView.as_view(), name='user_logout'),
    path('register_view/', views.register_view, name='register_view'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('edit_photo/<int:photo_id>/', views.EditUploadedPhoto.as_view(), name='edit_uploaded_photo'),
    path('edit_profile/picture/', views.UploadProfilePictureView.as_view(), name='upload_profile_picture'),
    path('edit_profile/details/', views.EditUserProfileDetailsView.as_view(), name='edit_user_profile_details'),
    path('<str:username>/user_gallery/', views.UserGalleryView.as_view(), name='user_gallery'),
    path('<str:username>/edit_gallery/', views.EditGalleryView.as_view(), name='edit_gallery'),
    path('upload_photo/', views.UploadPhotoView.as_view(), name='upload_photo'),
    path('newsfeed/', views.newsfeed, name='newsfeed'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
    path('accounts/', include(('allauth.urls', 'allauth'))),
    path('accounts/social/', include('allauth.socialaccount.urls')),
    path('orders/', marketplaceviews.all_products, name='orders'),
    # Cookie Consent
    path('cookie-consent/', views.cookie_consent, name='cookie_consent'),
    path('process_payment/', marketplaceviews.process_payment, name='process_payment'),

    # path('delete_profile/', views.delete_user_profile, name='delete_user_profile'),
    # path('delete_confirmation/', views.delete_confirmation, name='delete_confirmation'),
] \
    #               + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # to serve media when DEBUG = False:
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


handler404 = views.Custom404View.as_view()
handler500 = views.Custom500View.as_view()

# Serving media files during development only
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serving static files
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
