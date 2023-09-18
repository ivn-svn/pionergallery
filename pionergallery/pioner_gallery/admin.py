from django.contrib import admin
from .models import Category, Article
from .forms import ArticleForm

admin.site.register(Category)
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    form = ArticleForm
