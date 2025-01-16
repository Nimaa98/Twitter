from django.shortcuts import render , get_object_or_404 , redirect
from .models import Post,Comment,Like,Tag, PostImage,PostTag
from django.views.generic import View
from .form import PostForm , CommentForm
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from Core.models import Image

# Create your views here.


class PostListView(View):
    
    def get(self, request):

        post_list = Post.objects.all()
        like_symble = Image.objects.filter(name = 'like').first()
        comment_symble = Image.objects.filter(name = 'comment').first()
        template = 'Contents/list_post.html'
        context = {"post_list" : post_list , "like" : like_symble , "comment" : comment_symble}

        return render (
            request= request,
            template_name = template,
            context= context,
            )

class PostDetailView(View):
    def get(self):
        pass


class TagView(View):
    def get(self):
        pass