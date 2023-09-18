from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from pioner_gallery.webapp.models import Article, Category
from .forms import ArticleForm
from django.db.models import Q
from datetime import datetime
from django.urls import reverse
from django.utils.timezone import now


class ArticlesListView(ListView):
    model = Article
    template_name = 'pioner_gallery/articles/list.html'
    context_object_name = 'articles'
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()
        sort_by = self.request.GET.get('sort')
        search_query = self.request.GET.get('q')

        if search_query:
            queryset = queryset.filter(Q(title__icontains=search_query) | Q(category__name__icontains=search_query))

        if sort_by == 'created_at':
            queryset = queryset.order_by('-created_at')
        elif sort_by == 'category':
            queryset = queryset.order_by('category__name')

        return queryset


class ArticlesByDateAndCategoryListView(ListView):
    template_name = 'pioner_gallery/articles/list.html'
    context_object_name = 'articles'
    paginate_by = 6

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        date_str = self.kwargs.get('date_str')
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()

        queryset = Article.objects.filter(
            Q(category__id=category_id) & Q(created_at__date=date_obj)
        )
        return queryset


def list_articles(request):
    category_id = request.GET.get('category')
    search_query = request.GET.get('q')

    articles = Article.objects.all()

    if category_id:
        articles = articles.filter(category__id=category_id)

    if search_query:
        articles = articles.filter(Q(title__icontains=search_query) | Q(category__name__icontains=search_query))

    context = {
        'articles': articles,
        'categories': Category.objects.all(),
    }

    return render(request, 'pioner_gallery/articles/list.html', context)


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'pioner_gallery/articles/detail.html'
    context_object_name = 'article'



class ArticleCreateView(CreateView):
    model = Article
    template_name = 'pioner_gallery/articles/create.html'
    form_class = ArticleForm

    def form_valid(self, form):

        article = form.save(commit=False)


        article.created_at = now()  # Use Django's timezone.now() to get the current time

        # Save the article instance
        article.save()


        return redirect('ArticleDetailView', pk=article.pk)

    def get_success_url(self):
        # If for some reason 'ArticleDetailView' is not a valid name, you can use reverse here too
        return reverse('ArticleDetailView', kwargs={'pk': self.object.pk})


class ArticleUpdateView(UpdateView):
    model = Article
    template_name = 'pioner_gallery/articles/update.html'
    form_class = ArticleForm
    context_object_name = 'article'
    success_url = reverse_lazy('list_articles_blog')


class ArticleDeleteView(DeleteView):
    model = Article
    template_name = 'pioner_gallery/articles/delete.html'
    context_object_name = 'article'
    success_url = reverse_lazy('list_articles_blog')
