from .models import User
from .utils import Util
from .serializers import customRegisterSerializer, customLoginSerializer, customTokenRefreshSerializer, userProfileSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.urls import reverse
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
import jwt

class customSignUpView (GenericAPIView) :
    serializer_class = customRegisterSerializer

    def post (self, request) :
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = User.objects.get(email=serializer.data['email'])

        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(request).domain
        relativeLink = reverse('emailVerify')
        
        absurls = F'http://{current_site}{relativeLink}?token={token}'
        email_body = F'Hi {user.username} Use link below to verify your email \n{absurls}'
        data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'Verify your email'}
        Util.send_email(data)
        
        return Response({'message': '이메일을 확인하세요'}, status=201)

class customLoginView (TokenObtainPairView) :
    serializer_class = customLoginSerializer
        
class customRefreshView (TokenRefreshView) :
    serializer_class = customTokenRefreshSerializer

class VerifyEmail (GenericAPIView) :

    def get (self, request) :
        token = request.GET.get('token')

        try :
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified :
                user.is_verified = True
                user.save()
            return Response({'message': '성공적으로 인증되었습니다'})

        except jwt.ExpiredSignatureError :
            return Response({'message': '인증이 만료되었습니다'}, status=400)
        
        except jwt.exceptions.DecodeError :
            return Response({'message': '잘못된 토큰입니다'}, status=400)

class userProfileView (ModelViewSet) :
    serializer_class = userProfileSerializer
    permission_classes = [IsAuthenticated]

    def list (self, request) :
        queryset = User.objects.filter(email=self.request.user)
        serializer = userProfileSerializer(queryset, many=True)

        for i in serializer.data :
            return Response(i)