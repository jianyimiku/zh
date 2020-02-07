from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_http_methods
from django.views.generic import CreateView, ListView, DetailView
from django.utils.decorators import method_decorator

from zh.helpers import ajax_required
from qa.models import Question, Answer
from qa.form import QuestionForm

from notifications.views import notification_handler


class QuestionListView(LoginRequiredMixin, ListView):
    """所有问题页"""

    queryset = Question.objects.select_related('user')
    paginate_by = 10
    context_object_name = "questions"
    template_name = "qa/question_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(QuestionListView, self).get_context_data()
        context["popular_tags"] = Question.objects.get_counted_tags()  # 页面的标签功能
        context["active"] = "all"
        return context


class AnsweredQuetionListView(QuestionListView):
    def get_queryset(self):
        return Question.objects.get_answered()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AnsweredQuetionListView, self).get_context_data()
        context["popular_tags"] = Question.objects.get_counted_tags()  # 页面的标签功能
        context["active"] = "answered"
        return context


class UnansweredQuetionListView(QuestionListView):
    def get_queryset(self):
        return Question.objects.get_unanswered()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UnansweredQuetionListView, self).get_context_data()
        context["popular_tags"] = Question.objects.get_counted_tags()  # 页面的标签功能
        context["active"] = "unanswered"
        return context


class CreateQuestionView(LoginRequiredMixin, CreateView):
    model = Question
    form_class = QuestionForm
    template_name = "qa/question_form.html"
    message = "问题已经提交"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateQuestionView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse_lazy("qa:unanswered_q")


class QuestionDetailView(LoginRequiredMixin, DetailView):
    model = Question
    context_object_name = 'question'
    template_name = 'qa/question_detail.html'

# def get_context_data(self, **kwargs):
#     content = super().get_context_data(**kwargs)
#     question_id = self.kwargs['pk']
#     question = Question.objects.get(pk=question_id)
#     users = question.votes.values_list('user', flat=True)  # 当前问题的所有投票用户
#     if self.request.user.pk in users:
#         content['status'] = (question.votes.get(user=self.request.user).value == 'U')
#     print(content)
#     return content


class CreateAnswerView(LoginRequiredMixin, CreateView):
    """回答问题"""
    model = Answer
    fields = ['content', ]
    message = '您的问题已提交'
    template_name = 'qa/answer_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.question_id = self.kwargs['question_id']
        return super(CreateAnswerView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse_lazy('qa:question_detail', kwargs={"pk": self.kwargs['question_id']})

@login_required
@ajax_required
@require_http_methods(["POST"])
def question_vote(request):
    """给问题投票，AJAX POST请求"""
    question_id = request.POST["question"]
    value = True if request.POST["value"] == 'U' else False  # 'U'表示赞，'D'表示踩
    question = Question.objects.get(pk=question_id)
    users = question.votes.values_list('user', flat=True)  # 当前问题的所有投票用户
    if request.user.pk in users and (question.votes.get(user=request.user).value == value):
        question.votes.get(user=request.user).delete()
    else:
        question.votes.update_or_create(user=request.user, defaults={"value": value})
    return JsonResponse({"votes": question.total_votes()})


@login_required
@ajax_required
@require_http_methods(["POST"])
def answer_vote(request):
    """给回答投票，AJAX POST请求"""
    answer_id = request.POST["answer"]
    value = True if request.POST["value"] == 'U' else False  # 'U'表示赞，'D'表示踩
    answer = Answer.objects.get(uuid_id=answer_id)
    users = answer.votes.values_list('user', flat=True)  # 当前回答的所有投票用户

    if request.user.pk in users and (answer.votes.get(user=request.user).value == value):
        answer.votes.get(user=request.user).delete()
    else:
        answer.votes.update_or_create(user=request.user, defaults={"value": value})

    return JsonResponse({"votes": answer.total_votes()})

@login_required
@ajax_required
@require_http_methods(["POST"])
def accept_answer(request):
    """
    接受回答，AJAX POST请求
    已经被接受的回答用户不能取消
    """
    answer_id = request.POST["answer"]
    answer = Answer.objects.get(pk=answer_id)
    # 如果当前登录用户不是提问者，抛出权限拒绝错误
    if answer.question.user.username != request.user.username:
        raise PermissionDenied
    answer.accept_answer()
    notification_handler(request.user, answer.user, 'W', answer)
    return JsonResponse({'status': 'true'}, status=200)
