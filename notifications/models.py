import uuid

from django.core import serializers
from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from slugify import slugify


class NotificationQuerySet(models.query.QuerySet):

    def unread(self):
        return self.filter(unread=True)

    def read(self):
        return self.filter(unread=False)

    def mark_all_as_read(self, recipient=None):

        qs = self.unread()
        if recipient:
            qs = qs.filter(recipient=recipient)
        return qs.update(unread=False)

    def mark_all_as_unread(self, recipient=None):

        qs = self.unread()
        if recipient:
            qs = qs.filter(recipient=recipient)
        return qs.update(unread=True)

    def get_most_recent(self, recipient=None):
        qs = self.unread()[:5]
        if recipient:
            qs = qs.filter(recipient=recipient)[:5]
        return qs

    def serialize_latest_notifications(self, recipient=None):
        """序列化最近5条未读通知，可以传入接收者参数"""
        qs = self.get_most_recent(recipient)
        notification_dic = serializers.serialize('json', qs)
        return notification_dic



class Notification(models.Model):
    NOTIFICATION_TYPE = (
        ('L', '赞了'),
        ('C', '评论了'),
        ('F', '收藏了'),
        ('A', '回答了'),
        ('W', '接受了回答'),
        ('R', '回复了'),
        ('I', '登录'),
        ('O', '退出')
    )
    uuid_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="nofity_actor", on_delete=models.CASCADE,
                              verbose_name="触发者")
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, related_name="notifications",
                                 on_delete=models.CASCADE, verbose_name="接受者")
    unread = models.BooleanField(default=True, db_index=True, verbose_name="未读")
    slug = models.SlugField(max_length=80, null=True, blank=True, verbose_name="(URL)别名")
    verb = models.CharField(max_length=1, choices=NOTIFICATION_TYPE, verbose_name="通知")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    content_type = models.ForeignKey(ContentType, related_name="notify_action_object", null=True, blank=True,
                                     on_delete=models.CASCADE)
    object_id = models.CharField(max_length=255, null=True, blank=True)
    action_object = GenericForeignKey()
    objects = NotificationQuerySet.as_manager()

    class Meta:
        verbose_name = "通知"
        verbose_name_plural = verbose_name
        ordering = ("-created_at", )



    def __str__(self):
        if self.action_object:
            return f'{self.actor}{self.get_verb_display()}{self.action_object}'
        return f'{self.actor}{self.get_verb_display()}'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.slug:
            self.slug = slugify(f'{self.recipient}{self.uuid_id}{self.verb}')
            super(Notification, self).save()

    def mark_as_read(self):
        if self.unread:
            self.unread = False
            self.save()

    def mark_as_unread(self):
        if not self.unread:
            self.unread = True
            self.save()