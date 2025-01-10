from django.shortcuts import render , get_object_or_404
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
    

class UserDetailView(View):
    
    def get(self, request, pk):

        user_detail = get_object_or_404(User , pk=pk)

        template = 'Users/detail_user.html'
        context = {"user_detail" : user_detail}

        return render (
            request= request,
            template_name = template,
            context= context,
            )