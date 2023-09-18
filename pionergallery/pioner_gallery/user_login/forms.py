from django import forms
from .models import UserProfile
from django import forms
from .models import UserPhoto


class UserPhotoForm(forms.ModelForm):
    class Meta:
        model = UserPhoto
        fields = ('photo_name', 'photo', 'author', 'price', 'category', 'subcategory', 'location_taken', 'description')


class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'username', 'email', 'phone', 'mobile', 'address', 'job_title', 'city',
                  'state', 'country', 'website', 'github_username', 'twitter_username', 'instagram_username', 'facebook_username']
