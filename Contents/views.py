from django.shortcuts import render , get_object_or_404 , redirect
from .models import Post,Comment,Like,Tag, PostImage,PostTag
from django.views.generic import View
from .form import PostForm , CommentForm
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from Core.models import Image
from django.http import JsonResponse


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

class CommentListView(View):

    def get(self, request, pk):
        
        post = get_object_or_404(Post , pk=pk)

        comment_list = post.post_comment.filter(parent = None)
        like_symble = Image.objects.filter(name = 'like').first()
        comment_symble = Image.objects.filter(name = 'comment').first()

        template = 'Contents/list_comment.html'
        context = {"post" : post , "comments": comment_list,"like" : like_symble , "comment" : comment_symble}
            
        return render (
                request= request,
                template_name = template,
                context= context,
                )
        


class TagView(View):
    def get(self):
        pass


class LikeView(LoginRequiredMixin,View):

    def post(self, request, pk):
        if request.method == "POST":
            post = get_object_or_404(Post, pk=pk)
            
            if post.is_liked(request.user, post):
                post.dislike(request.user,post)
            else:
                post.like(request.user,post)

            post.save()
            return JsonResponse({'likes': post.count_likes()}) 
        return JsonResponse({'error': 'Invalid request method'}, status=400)