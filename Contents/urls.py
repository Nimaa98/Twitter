from .views import PostListView , PostDetailView , TagView
from django.urls import path



app_name = 'Contents'
urlpatterns = [
    path('contents/' , PostListView.as_view() , name = 'post-list'),
    path('posts/<uuid:pk>/' , PostDetailView.as_view() , name = 'detail-post'),
    path('tags/<uuid:pk>/' , TagView.as_view(), name = 'tag'),

]