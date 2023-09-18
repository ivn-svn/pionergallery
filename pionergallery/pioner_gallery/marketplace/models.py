from django.contrib.auth.models import User
from django.db import models

from pioner_gallery.user_login.models import UserPhoto


class ArticleProduct(models.Model):
    name = models.CharField(max_length=30)
    created_on = models.DateTimeField(auto_now_add=True)


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Cart"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    photo = models.ForeignKey(UserPhoto, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)  # This allows for future flexibility if you want to buy multiple copies

    def __str__(self):
        return f"{self.photo.photo_name} in {self.cart.user.username}'s Cart"
