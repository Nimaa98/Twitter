from django.shortcuts import render , get_object_or_404
from .models import User
from django.views.generic import View
from .form import LoginForm



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
    

class UserDetailView(View):
    
    def get(self, request, pk):

        user_detail = get_object_or_404(User , pk=pk)
        print(request.user)

        template = 'Users/detail_user.html'
        context = {"user_detail" : user_detail}

        return render (
            request= request,
            template_name = template,
            context= context,
            )
    

class LoginView(View):

    def get(self,request):
        form = LoginForm

        template = 'Users/login.html'
        context = {'from': form}

        return render (
            request= request,
            template_name = template,
            context= context,
            )