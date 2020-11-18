from django.urls import path, include
from .views import *

urlpatterns = [
    path('post', CreatePostView.as_view({'post': 'create'})),
    path('post/all', ReadAllListPostView.as_view({'get': 'list'})),
    path('post/popular', ReadPopularListPostView.as_view({'get': 'list'})),
    path('post/follow', ReadFollowingPostView.as_view({'get': 'list'})),
    path('post/<int:pk>', ReadOneUpdateDeletePostView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('post/<int:post_id>/comment', CreateCommentView.as_view({'post': 'create'})),
    path('post/<int:post_id>/comments', ReadCommentView.as_view({'get': 'list'})),
    path('post/<int:post_id>/comment/<int:pk>', UpdateDeleteCommentView.as_view({'put': 'update', 'delete': 'destroy'})),
    path('post/<int:post_id>/like', LikeView.as_view()),
    path('post/<int:post_id>/likes', ReadLikerView.as_view({'get': 'list'}))
]