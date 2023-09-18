from django.core.exceptions import ObjectDoesNotExist
from .models import UserProfile

def user_profile(request):
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            return {'user_profile': user_profile}
        except ObjectDoesNotExist:
            return {}
    else:
        return {}


def cookie_consent(request):
    user_consent = None
    if request.user.is_authenticated:
        user_consent = request.user.userprofile.cookie_consent
    else:
        user_consent = request.session.get('cookie_consent')

    return {
        'user_consent': user_consent
    }
