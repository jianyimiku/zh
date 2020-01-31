from django.db import models
from users.models import User
from slugify import slugify
from taggit.managers import TaggableManager
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify

# Create your models here.
class ArticleQuerySet(models.query.QuerySet):
    ''' 自定义QuerySet, 提高模型类的可用性  '''

    def get_published(self):
        ''' 获取已发表的文章 '''
        return self.filter(status="P")

    def get_drafts(self):
        ''' 获取草稿箱的文章 '''
        return self.filter(status="D")

    def get_counted_tags(self):
        ''' 统计所有已经发表的文章，每一个标签的数量(大于0的) '''
        tag_dict = {}
        query = self.get_published().annotate(tagged=models.Count('tags')).filter(tagged__gt=0)
        for obj in query:
            for tag in obj.tags.names():
                if tag not in tag_dict:
                    tag_dict[tag] = 1
                else:
                    tag_dict[tag] += 1
        return tag_dict.items()


class Article(models.Model):
    STATUS = (("D", "Draft"), ("P", "Published"))
    title = models.CharField(max_length=255, unique=True, verbose_name="标题")
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="author",
                             verbose_name="作者")
    image = models.ImageField(upload_to="articles_picture/%Y/%m/%d/", verbose_name="文章图片")
    slug = models.SlugField(max_length=255, verbose_name="(URL)别名")
    status = models.CharField(max_length=1, choices=STATUS, default="D", verbose_name="状态")
    content = MarkdownxField(verbose_name="内容")
    edited = models.BooleanField(default=False, verbose_name="是否可编辑")
    tags = TaggableManager(help_text="多个标签使用逗号隔开,(英文)", verbose_name="标签")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    objects = ArticleQuerySet.as_manager()

    class Meta:
        verbose_name = "文章"
        verbose_name_plural = verbose_name
        ordering = ("created_at",)

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.slug = slugify(self.title)
        super().save()

    def get_markdown(self):
        ''' 讲markdown文本转换成html  '''
        return markdownify(self.content)
