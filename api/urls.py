from django.urls import path, include
from .views import customSignUpView, customLoginView, customRefreshView, VerifyEmail
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('signUp', customSignUpView.as_view()),
    path('emailVerify', VerifyEmail.as_view(), name='emailVerify'),
    path('login', customLoginView.as_view()),
    path('renewalToken', customRefreshView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)