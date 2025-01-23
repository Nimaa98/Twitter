from django.shortcuts import render , get_object_or_404 , redirect
from .models import Post,Comment,Like,Tag, PostImage,PostTag, Follow_Tag ,Archive
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
        


class TagView(LoginRequiredMixin,View):


    like_symble = Image.objects.filter(name = 'like').first()
    comment_symble = Image.objects.filter(name = 'comment').first()

    template = 'Contents/tag.html'

    def get(self, request,pk):

        tag = Tag.objects.get(pk=pk)
        post_list = Post.objects.filter(tags=tag)

        tag.is_followed = Follow_Tag.is_following(request.user,tag)

        context = {"post_list" : post_list , "like" : self.like_symble , "comment" : self.comment_symble, "tag":tag}
        return render (
            request= request,
            template_name = self.template,
            context= context,
            )

    def post(self, request,pk):

        tag = Tag.objects.get(pk=pk)
        post_list = Post.objects.filter(tags=tag)
        
        print(request.POST)
        if request.POST["action"] == "follow":
            
            Follow_Tag.follow(request.user,tag)
        else:
            
            Follow_Tag.unfollow(request.user,tag)

        return redirect('Contents:tag' ,tag.id)





class FavoritTagView(LoginRequiredMixin,View):
   
    post_list=[]

    def get(self, request):

        like_symble = Image.objects.filter(name = 'like').first()
        comment_symble = Image.objects.filter(name = 'comment').first()

        template = 'Contents/favorit_tags.html'

        followed_tags = Follow_Tag.objects.filter(follower_user=request.user).values_list('following_tag',flat=True)
        
        unique_posts = set()

        for tag in followed_tags:
            single_post_list = Post.objects.filter(tags= tag)
            unique_posts.update(single_post_list)
        
            self.post_list = sorted(unique_posts , key=lambda post: post.create_at , reverse=True)
        
        numbers = False
        if len(self.post_list) == 0:
            numbers = True

    
        context = {"post_list" : self.post_list , "like" : like_symble , "comment" : comment_symble, "numbers":numbers}
        return render (
            request= request,
            template_name = template,
            context= context,
            )




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
    

class CommentFormView(LoginRequiredMixin,View):
    
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
    


class PostFormView(LoginRequiredMixin,View):
    form = PostForm

    def get(self, request):
        template = 'Contents/post.form.html'
        context = {"form": self.form(initial={'user': request.user})}
        return render(request=request, template_name=template, context=context)

    def post(self, request):
        form = self.form(request.POST, request.FILES)
        

        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()

            images = request.FILES.getlist('images')
            Image.make_iamge(images,post)
        
            
            tags = request.POST.get('tags','')            
            Tag.make_tag(tags,post)

            messages.success(request, 'پست شما با موفقیت ثبت شد!')
            return redirect('Contents:post-list')
        else:
            messages.error(request, 'در وارد کردن اطلاعات دقت کنید!')
        return redirect('Contents:post-form')


class ArchivePostView(LoginRequiredMixin,View):

    def post(self,request,pk):
        user = request.user
        post = get_object_or_404(Post,pk=pk)


        if request.POST["action"] == "save" and not Archive.is_save(user,post):
            Archive.add_post(user,post)

        else:
            Archive.remove_post(user,post)

        return redirect('Contents:get-archives')
      
class ArchiveGetView(LoginRequiredMixin,View):
    
    def get(self,request):

        user = request.user
        
        post_list = Archive.take_posts(user)

        for post in post_list:
            post.is_saved = Archive.is_save(user , post)


        like_symble = Image.objects.filter(name = 'like').first()
        comment_symble = Image.objects.filter(name = 'comment').first()
        template = 'Contents/archive.html'
        context = {"post_list" : post_list , "like" : like_symble , "comment" : comment_symble}


        return render (
            request= request,
            template_name = template,
            context= context,
            )