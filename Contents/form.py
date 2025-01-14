from django import forms
from .models import Post , Tag ,Comment
from Core.models import Image


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title','text','tags','images']

    tags = forms.ModelMultipleChoiceField(
            queryset = Tag.objects.all(),
            widget = forms.CheckboxSelectMultiple,
            required = False
        )

    images = forms.ModelMultipleChoiceField(
            queryset = Image.objects.all(),
            widget = forms.CheckboxSelectMultiple,
            required = False
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


