from django import forms
from django.db import models
from .models import Post , Tag ,Comment
from Core.models import Image
from django.forms.widgets import ClearableFileInput


from django.forms.widgets import ClearableFileInput




class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'text', 'tags', 'images']
    
    tags = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'تگها را با کاما جدا کنید'}),
        required=False
    )
    

    images = forms.FileField(
        widget=ClearableFileInput,
        required=False
    )
    



class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['text' , 'post', 'user', 'parent']
    
        widgets = {
            'text': forms.Textarea(attrs={'placeholder': 'نظر خود را وارد کنید' , 'rows':3}),
            'post': forms.HiddenInput(),
            'user': forms.HiddenInput(),
            'parent': forms.HiddenInput(),
        }



    