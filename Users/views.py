from django.shortcuts import render , get_object_or_404 , redirect
from .models import User
from django.views.generic import View
from .form import LoginForm
from django.contrib.auth import authenticate , login
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages



# Create your views here.


class UserListView(View):

    def get(self, request):
        

        user_list = User.objects.all()
        print(request.user)
        template = 'Users/list_user.html'
        context = {"user_list" : user_list}

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

    def get(self,request):
        form = LoginForm

        template = 'login.html'
        context = {"form": form}

        return render (
            request= request,
            template_name = template,
            context= context,
            )
    
    def post(self,request):
        
        form = LoginForm(request.POST)

        template = 'login.html'
        context = {"form": form}

        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request,
                username = cd["name"],
                password = cd["password"],
            )

        if user:
            login(request,user)
            return redirect ('Users:user-list')

        messages.error(request,'invalid input')
        return redirect('Users:login')
