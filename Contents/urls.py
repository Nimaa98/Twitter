from .views import PostListView , CommentListView , TagView , LikeView
from django.urls import path



app_name = 'Contents'
urlpatterns = [
    path('contents/' , PostListView.as_view() , name = 'post-list'),
    path('comments/<uuid:pk>/' , CommentListView.as_view() , name = 'comment-list'),
    path('like/<uuid:pk>/' , LikeView.as_view() , name = 'like'),
    path('tags/<uuid:pk>/' , TagView.as_view(), name = 'tag'),

]