from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def profile_picture_url(user_profile):
    if user_profile.profile_picture and hasattr(user_profile.profile_picture, 'url'):
        return user_profile.profile_picture.url
    else:
        return f"{settings.STATIC_URL}images/noprofile.gif"
