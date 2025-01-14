from .views import UserListView , UserDetailView , LoginView
from django.urls import path


app_name = 'Users'
urlpatterns = [
    path('users/' , UserListView.as_view() , name = 'user-list'),
    path('users/<uuid:pk>/' , UserDetailView.as_view() , name = 'detail-user'),
    path('login/' , LoginView.as_view() , name = 'login'),

]

