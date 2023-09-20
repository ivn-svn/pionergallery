from django.contrib import admin
from pioner_gallery.webapp.models import Article, Category
from django.forms import modelform_factory
from .forms import ArticleForm
from .models import BlogPost


admin.site.register(Category)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    form = ArticleForm


class BlogPostAdmin(admin.ModelAdmin):
    # 1. Custom List Display
    list_display = ('title', 'author', 'created_at', 'updated_at')

    # 2. Filters on the right side
    list_filter = ('author', 'created_at', 'updated_at')

    # 3. Search functionality
    search_fields = ('title', 'content', 'author')

    # 4. Ordering
    ordering = ('-created_at',)

    # 5. Date Hierarchy (Navigate by dates)
    date_hierarchy = 'created_at'


admin.site.register(BlogPost, BlogPostAdmin)
