from django import forms

from .models import Comment, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "body", "is_published")
        widgets = {"body": forms.Textarea(attrs={"rows": 8})}
        help_texts = {"is_published": "Опубликованный пост появляется в общем списке."}


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("text",)
        widgets = {"text": forms.Textarea(attrs={"rows": 3})}
