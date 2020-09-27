from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from api.views import userProfileView
from rest_framework import permissions

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('api.urls')),
    path('feed/', include('feed.urls')),
    path('user', userProfileView.as_view({'get': 'list'})),
]
