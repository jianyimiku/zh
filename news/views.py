# Create your views here.

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DeleteView
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import News
from zh.helpers import ajax_required, AuthorRequireMixin
from django.urls import reverse_lazy


class NewsListView(LoginRequiredMixin, ListView):
    ''' 首页动态 '''
    model = News
    paginate_by = 5  # 分页每页现实多少个状态
    template_name = 'news/news_list.html'

    def get_queryset(self):
        return News.objects.filter(reply=False)


@login_required
@ajax_required
@require_http_methods(['POST'])
def post_new(request):
    ''' 发送动态 AJAX POST请求 '''
    post = request.POST['post'].strip()
    if post:
        posted = News.objects.create(
            user=request.user,
            content=post,
        )
        html = render_to_string('news/news_single.html', {"news": posted, 'request': request})
        return HttpResponse(
            html)  # return render(request, 'news/news_single.html', {"news": posted, 'request': request}) 也是ok
    else:
        return HttpResponseBadRequest("内容不能为空")


@login_required
@ajax_required
@require_http_methods(['POST'])
def like(request):
    """ 点赞 """
    news_id = request.POST['news']
    news = News.objects.get(pk=news_id)
    # 取消或者添加赞
    news.switch_like(request.user)
    return JsonResponse({"likes": news.count_likers()})


@login_required
@ajax_required
@require_http_methods(['GET'])
def get_thread(request):
    ''' 返回动态评论 '''
    news_id = request.GET['news']
    news = News.objects.get(pk=news_id)
    news_html = render_to_string("news/news_single.html", {"news": news})
    thread_html = render_to_string("news/news_thread.html", {"thread": news.get_thread(), 'request': request})
    return JsonResponse({
        "uuid": news_id,
        "news": news_html,
        "thread": thread_html,
    })


@login_required
@ajax_required
@require_http_methods(['POST'])
def post_comment(request):
    ''' 评论 '''
    post = request.POST['reply'].strip()
    parent_id = request.POST['parent']
    parent = News.objects.get(pk=parent_id)
    if post:
        parent.reply_this(request.user, post)
        return JsonResponse({"comments": parent.comment_count()})
    else:
        return HttpResponseBadRequest("内容不能为空")


class NewsDeleteView(LoginRequiredMixin, AuthorRequireMixin, DeleteView):
    model = News
    template_name = 'news/news_confirm_delete.html'
    # slug_url_kwarg = 'slug' # 通过url传入要删除的主键id 默认值是slug
    # pk_url_kwarg = 'pk' # 通过url传入要删除的主键id 默认值是pk
    success_url = reverse_lazy("news:list")  # 在项目URLConf未加载前使用
