from django.urls import path, include
from .views import CreateReadPostView, UpdateDeletePostView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('post', CreateReadPostView.as_view({'post': 'create', 'get': 'list'})),
    path('post/<int:pk>', UpdateDeletePostView.as_view({'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
    # path('post/<int:post.pk>/comments', CreateReadCommentView.as_view({'post': 'create', 'get': 'list'})),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)