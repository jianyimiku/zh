from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from .models import Article
from django.contrib.auth.mixins import LoginRequiredMixin
from articles.forms import ArticleForm
from django.urls import reverse_lazy
from django.contrib import messages
from zh.helpers import AuthorRequireMixin
from django.shortcuts import reverse
# Create your views here.

class ArticleListView(LoginRequiredMixin, ListView):
    model = Article
    paginate_by = 10
    context_object_name = "articles"
    template_name = 'articles/article_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['popular_tags'] = Article.objects.get_counted_tags()
        return context

    def get_queryset(self):
        return Article.objects.get_published()


class DraftListView(ArticleListView):
    def get_queryset(self):
        return Article.objects.filter(user=self.request.user).get_drafts()


class ArticCreateView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'articles/article_create.html'
    messages = "您的文章已经创建成功"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.messages)  # 消息传给下一次请求
        return reverse_lazy("articles:list")


class ArticleDetailView(LoginRequiredMixin, DetailView):
    model = Article
    template_name = "articles/article_detail.html"


class ArticleEditView(LoginRequiredMixin, AuthorRequireMixin, UpdateView):
    model = Article
    message = "您的文章编辑成功"
    form_class = ArticleForm
    template_name = "articles/article_update.html"

    def form_valid(self, form):
        form.instance.user == self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse("articles:article", kwargs={"slug": self.get_object().slug})
