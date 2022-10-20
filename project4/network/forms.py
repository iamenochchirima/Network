from django import forms
from django.forms import ModelForm

from .models import Post

class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = ['body']

        widgets = {
            "body": forms.Textarea(attrs={'class': 'form-control', 'rows':3}),
        }
