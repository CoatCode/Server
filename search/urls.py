from django.urls import path, include
from .views import UserSearchView, PostSearchView

urlpatterns = [
    path('post', PostSearchView.as_view({'get': 'list'})),
    path('user', UserSearchView.as_view({'get': 'list'})),
]