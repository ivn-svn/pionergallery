from django.db import models

class BlogPost(models.Model):
    title = models.CharField(max_length=200, default="Untitled Post")
    content = models.TextField(default="This is placeholder content.")
    author = models.CharField(max_length=200, default="Anonymous")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
