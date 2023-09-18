from django.apps import AppConfig


class UserLoginConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pioner_gallery.user_login'  # Correct app name


def ready(self):
    import pioner_gallery.user_login.signals
