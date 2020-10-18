from django.urls import path, include
from .views import MyProfileView, UserProfileView, UsersPostView, FollowersView, FollowingsView, FollowView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', MyProfileView.as_view({'get': 'list'})),
    path('/<int:user_id>', UserProfileView.as_view({'get': 'list'})),
    path('/<int:user_id>/follow', FollowView.as_view()),
    path('/<int:user_id>/follower', FollowersView.as_view({'get': 'list'})),
    path('/<int:user_id>/following', FollowingsView.as_view({'get': 'list'})),
    path('/<int:user_id>/posts', UsersPostView.as_view({'get': 'list'})),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)