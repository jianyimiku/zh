from django.shortcuts import render
# Create your views here.
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User  # 映射的模型类
    template_name = "users/user_detail.html"  # 渲染到哪个模板
    slug_field = "username"  # 模型类里面包含slug的字段
    slug_url_kwarg = "username"  # url配置里面包含slug的关键字参数

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        user = User.objects.get(username=self.request.user.username)
        context['moments_num'] = user.publisher.filter(reply=False).count()
        context['article_num'] = user.author.filter(status='p').count()
        context['comment_num'] = user.publisher.filter(reply=True).count() + user.comment_comments.all().count()
        context['question_num'] = user.q_author.all().count()
        context['answer_num'] = user.a_author.all().count()

        tmp = set()
        set_num = user.sent_messages.all()
        for s in set_num:
            tmp.add(s.recipient.username)
        received_num = user.received_messages.all()
        for r in received_num:
            tmp.add(r.sender.username)

        context['interaction_num'] = user.liked_news.all().count() + user.qa_vote.all().count() + context['comment_num'] + len(tmp)

        return context

class UserUpdateView(LoginRequiredMixin, UpdateView):
    ''' 用户只能跟新自己的信息 '''
    model = User
    fields = ['nickname', 'email', 'picture', 'job_title', 'introduction', 'personal_url', 'weibo', 'zhihu', 'github',
              'linkedin']  # 允许用户更改的字段
    template_name = "users/user_form.html"

    def get_success_url(self):
        ''' 表示更新成功后跳转的页面 '''
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def get_object(self, queryset=None):
        return self.request.user
