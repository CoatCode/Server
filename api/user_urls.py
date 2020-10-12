from django.urls import path, include
from .views import UserProfileView, UserFollowingView, UserUnfollowingView, UsersPostView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', UserProfileView.as_view({'get': 'list'})),
    path('/<int:user_id>/follow', UserFollowingView.as_view({'post': 'create'})),
    path('/<int:user_id>/follow/<int:pk>', UserUnfollowingView.as_view({'delete': 'destroy'})),
    path('/posts', UsersPostView.as_view({'get': 'list'})),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)