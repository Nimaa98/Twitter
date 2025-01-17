from .views import PostListView , CommentListView , TagView
from django.urls import path



app_name = 'Contents'
urlpatterns = [
    path('contents/' , PostListView.as_view() , name = 'post-list'),
    path('comments/<uuid:pk>/' , CommentListView.as_view() , name = 'comment-list'),
    path('tags/<uuid:pk>/' , TagView.as_view(), name = 'tag'),

]