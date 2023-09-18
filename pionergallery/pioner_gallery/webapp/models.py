from django.db import models
from django.utils.html import strip_tags
from bs4 import BeautifulSoup
from django.contrib.auth.models import User

import math


class GalleryImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='')
    caption = models.CharField(max_length=100)

    def __str__(self):
        return self.caption


class Contact(models.Model):
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=254)
    message_subject = models.CharField(max_length=100, blank=True)
    message_body = models.TextField(max_length=3000, blank=True)


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=500, null=False)
    content = models.TextField(null=False)
    thumbnail = models.ImageField(upload_to='article_thumbnails/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'web_article'

    @property
    def reading_time(self):
        words_per_minute = 200  # Fixed reading speed of 200 words per minute

        clean_content = strip_tags(self.content)
        soup = BeautifulSoup(clean_content, 'html.parser')
        word_count = len(soup.get_text().split())

        minutes = word_count / words_per_minute
        return math.ceil(minutes)
