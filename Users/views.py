from django.shortcuts import render , get_object_or_404 , redirect
from .models import User
from django.views.generic import View
from .form import LoginForm
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages



# Create your views here.


class UserListView(View):

    def get(self, request):

        user_list = User.objects.all()
        template = 'Users/list_user.html'
        context = {"user_list" : user_list}

        return render (
            request= request,
            template_name = template,
            context= context,
            )
    
class UserProfileView(View):
    
    def get(self, request):
        user_list = User.objects.all()
        this_user = request.user
        for user in user_list:
            user.is_followed = this_user.is_following(this_user,user)

        
        template = 'Users/user_profile.html'
        context = {"this_user":request.user , "user_list": user_list}

        return render (
            request= request,
            template_name = template,
            context= context,
            )
    

class UserDetailView(LoginRequiredMixin,View):
    
    def get(self, request, pk):

        user_detail = get_object_or_404(User , pk=pk)
        
        template = 'Users/detail_user.html'
        context = {"user_detail" : user_detail}

        if request.user.username != user_detail.username:
            return redirect('Users:login')
            
        return render (
                request= request,
                template_name = template,
                context= context,
                )
    

class LoginView(View):

    form = LoginForm
    user_list = User.objects.all()

    def get(self,request):

        template = 'login.html'
        context = {"form": self.form}

        return render (
            request= request,
            template_name = template,
            context= context,
            )
    
    def post(self,request):
        
        form = self.form(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request,
                username = cd["name"],
                password = cd["password"],
            )

        if user:
            login(request,user)
            return redirect ('Users:user-profile')

        messages.error(request,'نام کاربری یا رمز عبور اشتباه است!')
        return redirect('Users:login')


class FollowView(LoginRequiredMixin,View):
    def post(self,request, pk):

        print(request.POST["action"])

        user = get_object_or_404(User,pk=pk)

        if request.POST["action"] == "follow":
            user.follow(request.user,user)
        else:
            user.unfollow(request.user,user)
        
        return redirect('Users:user-profile')
