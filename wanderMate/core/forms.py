from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['caption', 'tags', 'images']

    images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
