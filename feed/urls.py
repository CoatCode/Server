from django.urls import path, include
from .views import CreatePostView, ReadListPostView, ReadOnePostView, UpdateDeletePostView, CreateCommentView, ReadCommentView, UpdateDeleteCommentView, ReadLikerView, LikeView

urlpatterns = [
    path('post', CreatePostView.as_view({'post': 'create'})),
    path('post/<int:pk>', ReadOnePostView.as_view({'get': 'retrieve'})),
    path('post/all', ReadListPostView.as_view({'get': 'list'})),
    path('post/<int:pk>', UpdateDeletePostView.as_view({'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
    path('post/<int:post_id>/comment', CreateCommentView.as_view({'post': 'create'})),
    path('post/<int:post_id>/comments', ReadCommentView.as_view({'get': 'list'})),
    path('post/<int:post_id>/comment/<int:pk>', UpdateDeleteCommentView.as_view({'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
    path('post/<int:post_id>/like', LikeView.as_view()),
    path('post/<int:post_id>/likes', ReadLikerView.as_view({'get': 'list'}))
]