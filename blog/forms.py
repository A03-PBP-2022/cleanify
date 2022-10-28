from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

    def __str__(self):
        return ""
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

    def __str__(self):
        return ""