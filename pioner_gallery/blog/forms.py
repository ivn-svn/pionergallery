from django import forms
from pioner_gallery.webapp.models import Article
from ckeditor.widgets import CKEditorWidget
from django import forms


# from .models import Category
class ArticleForm(forms.ModelForm):
    title = forms.CharField(max_length=200)
    content = forms.CharField(widget=CKEditorWidget())
    author = forms.CharField(max_length=200)
    thumbnail = forms.ImageField()  # Add the thumbnail field

    class Meta:
        model = Article
        fields = '__all__'
