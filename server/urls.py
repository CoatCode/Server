from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from api.views import userProfileView
from rest_framework import permissions

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('api.urls')),
    path('feed/', include('feed.urls')),
    path('search/', include('search.urls')),
    path('user', userProfileView.as_view({'get': 'list'})),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)