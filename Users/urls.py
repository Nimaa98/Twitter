from .views import UserListView , UserDetailView , LoginView ,FollowView , UserProfileView , LogoutView ,DeletePostView , ReturnUserView
from django.urls import path
from django.contrib.auth.views import LogoutView


app_name = 'Users'
urlpatterns = [
    path('users/' , UserListView.as_view() , name = 'user-list'),
    path('users/<uuid:pk>/' , UserDetailView.as_view() , name = 'detail-user'),
    path('login/' , LoginView.as_view() , name = 'login'),
    path('follow/<uuid:pk>/' , FollowView.as_view() , name = 'follow-user'),
    path('users/login' , UserProfileView.as_view() , name = 'user-profile'),
    path('user/logout/' , LogoutView.as_view() , name = 'logout'),
    path('user/delete/' , DeletePostView.as_view() , name = 'soft-delete'),
    path('user/return/' , ReturnUserView.as_view() , name = 'soft-return')

]

