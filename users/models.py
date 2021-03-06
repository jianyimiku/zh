from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


# Create your models here.
class User(AbstractUser):
    '''自定义用户模型'''
    nickname = models.CharField(null=True, blank=True, max_length=255, verbose_name="昵称")
    job_title = models.CharField(max_length=50, null=True, verbose_name="职称")
    introduction = models.TextField(blank=True, null=True, verbose_name="简介")
    picture = models.ImageField(upload_to='image/', null=True, blank=True, verbose_name="头像")
    location = models.CharField(max_length=50, null=True, blank=True, verbose_name="城市")
    personal_url = models.URLField(max_length=255, null=True, blank=True, verbose_name="个人链接")
    weibo = models.URLField(max_length=255, blank=True, null=True, verbose_name='微博链接')  # 连接使用URL
    zhihu = models.URLField(max_length=255, blank=True, null=True, verbose_name='知乎链接')
    github = models.URLField(max_length=255, blank=True, null=True, verbose_name='Github链接')
    linkedin = models.URLField(max_length=255, blank=True, null=True, verbose_name='LinkedIn链接')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        '''返回详情页中的url路径 kwargs为传入的参数'''
        return reverse("user:detail", kwargs={"username": self.username})

    def get_profile_name(self):
        '''返回名字'''
        if self.nickname:
            return self.nickname
        else:
            return self.username
