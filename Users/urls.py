from .views import UserListView 
from django.urls import path



app_name = 'Users'
urlpatterns = [
    path('users/' , UserListView.as_view() , name = 'user-list')
]

