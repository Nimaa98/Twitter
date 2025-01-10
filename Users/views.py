from django.shortcuts import render 
from .models import User
from django.views.generic import View

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
    

