from django.urls import path, include
from .views import CreateReadPostView, UpdateDeletePostView, CreateReadCommentView, UpdateDeleteCommentView, CreateReadLikeView, GetLikeUnlikeView, DeleteLikeView

urlpatterns = [
    path('post', CreateReadPostView.as_view({'post': 'create'})),
    path('post/all', CreateReadPostView.as_view({'get': 'list'})),
    path('post/<int:pk>', UpdateDeletePostView.as_view({'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
    path('post/<int:post_id>/comment', CreateReadCommentView.as_view({'post': 'create'})),
    path('post/<int:post_id>/comments', CreateReadCommentView.as_view({'get': 'list'})),
    path('post/<int:post_id>/comment/<int:pk>', UpdateDeleteCommentView.as_view({'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
    path('post/<int:post_id>/like', CreateReadLikeView.as_view({'post': 'create'})),
    path('post/<int:post_id>/like', GetLikeUnlikeView.as_view({'get': 'list'})),
    path('post/<int:post_id>/like/<int:pk>', DeleteLikeView.as_view({'delete': 'destroy'})),
]