from django.contrib.auth.models import User
from django.db import models


def user_photos_path(instance, filename):
    # Upload the profile picture to the 'profile_pics' directory, with a filename based on the user's ID
    return f"{instance.user.username}/profile_pics/user_{instance.user.id}/{filename}"


class UserPhoto(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_photos')
    photo = models.ImageField(upload_to=user_photos_path, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='authored_photos')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
#
    photo_name = models.CharField(max_length=30, default="Default Photo Name")
    description = models.CharField(max_length=100, default="Default Description")
    image_url = models.CharField(max_length=900, blank=True)
    price = models.FloatField(default=0.0)
    quantity = models.IntegerField(default=1)
    category = models.CharField(max_length=30, default="Default Category")
    subcategory = models.CharField(max_length=30, default="Default Subcategory")
    location_taken = models.CharField(max_length=30, default="Unknown Location")


    def __str__(self):
        return f"{self.user.username}'s Photo {self.pk}"


def user_profile_picture_path(instance, filename):
    # Upload the profile picture to the 'profile_pics' directory, with a filename based on the user's ID
    return f"{instance.user.username}/user_photos/user_{instance.user.id}/{filename}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, default='Your First Name')
    last_name = models.CharField(max_length=100, default='Your Last Name')
    username = models.CharField(max_length=100, default='Your Username')
    subscribe = models.BooleanField(default=False)
    email = models.EmailField(default='user@example.com')
    phone = models.CharField(max_length=20, default='N/A', blank=True)
    mobile = models.CharField(max_length=20, default='N/A', blank=True)
    address = models.CharField(max_length=200, default='N/A', blank=True)
    job_title = models.CharField(max_length=100, default='N/A', blank=True)
    city = models.CharField(max_length=100, default='N/A', blank=True)
    state = models.CharField(max_length=100, default='N/A', blank=True)
    country = models.CharField(max_length=100, default='N/A', blank=True)
    website = models.URLField(default='https://www.example.com', blank=True)
    github_username = models.CharField(max_length=100, default='githubuser', blank=True)
    twitter_username = models.CharField(max_length=100, default='twitteruser', blank=True)
    instagram_username = models.CharField(max_length=100, default='instauser', blank=True)
    facebook_username = models.CharField(max_length=100, default='fbuser', blank=True)
    profile_picture = models.ImageField(upload_to=user_profile_picture_path, blank=True)
    cookie_consent = models.CharField(max_length=10, choices=[('accepted', 'Accepted'), ('declined', 'Declined')], null=True, blank=True)


    def __str__(self):
        return (
            f"User: {self.user}, First Name: {self.first_name}, Last Name: {self.last_name}, \n"
            f"Username: {self.username}, Subscribe: {self.subscribe}, Email: {self.email}, \n"
            f"Phone: {self.phone}, Mobile: {self.mobile}, Address: {self.address}, \n"
            f"Job Title: {self.job_title}, City: {self.city}, State: {self.state}, \n"
            f"Country: {self.country}, Website: {self.website}, GitHub Username: {self.github_username}, \n"
            f"Twitter Username: {self.twitter_username}, Instagram Username: {self.instagram_username}, \n"
            f"Facebook Username: {self.facebook_username}, Profile Picture: {self.profile_picture}\n"
        )
