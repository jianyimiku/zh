from django import forms
from .models import Article
from markdownx.fields import MarkdownxFormField


class ArticleForm(forms.ModelForm):
    image = forms.ImageField(required=False, label="文章图片")
    status = forms.CharField(widget=forms.HiddenInput())
    edited = forms.BooleanField(widget=forms.HiddenInput(), initial=False, required=False)
    content = MarkdownxFormField(label="动态内容")

    class Meta:
        model = Article
        fields = ['title', 'content', 'image', 'tags', 'status']

    # def __init__(self, *args, **kwargs):
    #     super(ArticleForm, self).__init__(*args, **kwargs)
    #     self.fields['image'].required = False
