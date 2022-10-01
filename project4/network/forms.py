from django import forms
from django.forms import ModelForm

from .models import Post

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ["body"]

        widgets = {
            "body": forms.Textarea(attrs={'class': 'form-control col-md-5 col-lg-6'}),
        }
