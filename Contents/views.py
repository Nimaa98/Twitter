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
    

class CommentFormView(View):
    
    form = CommentForm
    
    
    def get(self,request,pk, comment_pk):

        parent_comment = None

        if pk != comment_pk:
            parent_comment = get_object_or_404(Comment,pk=comment_pk)
        
            
        post = get_object_or_404(Post,pk=pk,)
        template = 'Contents/comment.form.html'
        context = {"form": self.form(initial={'post': post , 'user': request.user , 'parent': parent_comment})}

        return render (
            request= request,
            template_name = template,
            context= context,
            )
    
    def post(self,request,pk, comment_pk):
        
        form = self.form(request.POST)
        post = get_object_or_404(Post,pk=pk,)


        parent_comment = None
        
        if pk != comment_pk:
            parent_comment = get_object_or_404(Comment,pk=comment_pk)



        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.parent = parent_comment
            comment.save()
            messages.success(request, 'کامنت شما با موفقیت ثبت شد!')
            return redirect('Contents:comment-list' ,pk=pk)
        else:
            messages.error(request,'در وارد کردن اطلاعات دقت کنید!')

        return redirect('Contents:comment-form', pk=pk)






