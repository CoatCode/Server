from django.urls import path, include
from .views import postView, commentView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('post/post', postView.as_view({"get": "list", "post": "create"})),
    path('post/detail/<int:pk>', postView.as_view({"get": "retrieve", "patch": "partial_update", "delete": "destroy"})),
    path('comment/post', commentView.as_view({"get": "list", "post": "create"})),
    path('comment/detail/<int:pk>', commentView.as_view({"get": "retrieve", "patch": "partial_update", "delete": "destroy"})),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)