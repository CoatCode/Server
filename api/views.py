from .models import User, Follow
from feed.models import Post
from .permissions import IsFollower
from .utils import Util
from .serializers import *
from .authentication import CheckJWT
from feed.serializers import PostSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
import jwt
from datetime import datetime, timedelta

class customSignUpView (GenericAPIView) :
    serializer_class = customRegisterSerializer

    def post (self, request) :
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user = User.objects.get(email=serializer.data['email'])

        token = RefreshToken.for_user(user)
        token['email'] = user.email

        current_site = get_current_site(request).domain
        relativeLink = reverse('emailVerify')
        
        absurls = F'http://{current_site}{relativeLink}?token={token}'
        email_body = F'Hi {user.username} Use link below to verify your email \n{absurls}'
        data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'Verify your email'}
        Util.send_email(data)
        
        return Response({'success': '이메일을 확인하세요.'}, status=201)

class customLoginView (GenericAPIView) :
    serializer_class = customLoginSerializer

    def post (self, request) :
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.get(email=serializer.data['email'])

        token = RefreshToken.for_user(user)
        token['email'] = user.email

        user.refresh_token_expires_at = str((datetime.now() + timedelta(weeks=1)).astimezone().replace(microsecond=0).isoformat())
        user.save(update_fields=('refresh_token_expires_at', ))

        data = {}

        data['token_type'] = settings.SIMPLE_JWT['AUTH_HEADER_TYPES'][0]
        data['access_token'] = str(token.access_token)
        data['expires_at'] = str((datetime.now() + timedelta(minutes=30)).astimezone().replace(microsecond=0).isoformat())
        data['refresh_token'] = str(token)
        data['refresh_token_expires_at'] = user.refresh_token_expires_at

        return Response(data)

class customRefreshView (GenericAPIView) :
    serializer_class = customTokenRefreshSerializer

    def post (self, request) :
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try :
            token = RefreshToken(serializer.data['refresh'])

        except :
            return Response({'detail': '잘못된 refresh token 입니다.'}, status=401)

        user = CheckJWT.get_user(token)

        data = {}

        data['token_type'] = settings.SIMPLE_JWT['AUTH_HEADER_TYPES'][0]
        data['access_token'] = str(token.access_token)
        data['expires_at'] = str((datetime.now() + timedelta(minutes=30)).astimezone().replace(microsecond=0).isoformat())
        data['refresh_token'] = str(token)
        data['refresh_token_expires_at'] = user.refresh_token_expires_at

        return Response(data, status=200)

class VerifyEmail (GenericAPIView) :

    def get (self, request) :
        token = request.GET.get('token')

        try :
            user = CheckJWT.get_user(token)

            if not user.is_verified :
                user.is_verified = True
                user.save()
            return Response({'success': '성공적으로 인증되었습니다.'})

        except jwt.ExpiredSignatureError :
            return Response({'detail': '인증이 만료되었습니다.'}, status=400)
        
        except jwt.exceptions.DecodeError :
            return Response({'detail': '잘못된 토큰입니다.'}, status=400)

class FollowersView (ModelViewSet) :
    serializer_class = userProfileSerializer
    permission_classes = [IsAuthenticated]
    queryset = Follow.objects.all()

    def get_queryset (self) :
        return super().get_queryset().filter(user_id=self.kwargs.get('user_id'))

    def list (self, request, *args, **kwargs) :
        followers = self.queryset.filter(following_user_id=self.kwargs.get('user_id')).values()
        data = []

        for follower in followers :
            userId = follower.get('user_id_id')
            user = User.objects.filter(pk=userId)
            serializer = self.serializer_class(user, many=True)

            if serializer.data == [] :
                break

            data.append(serializer.data[0])

        return Response(data)

class FollowingsView (ModelViewSet) :
    serializer_class = userProfileSerializer
    permission_classes = [IsAuthenticated]
    queryset = Follow.objects.all()

    def get_queryset (self) :
        return super().get_queryset().filter(user_id=self.kwargs.get('user_id'))

    def list (self, request, *args, **kwargs) :
        followers = self.queryset.filter(user_id=self.kwargs.get('user_id')).values()
        data = []

        for follower in followers :
            userId = follower.get('following_user_id_id')
            user = User.objects.filter(pk=userId)
            serializer = self.serializer_class(user, many=True)

            if serializer.data == [] :
                break

            data.append(serializer.data[0])

        return Response(data)

class FollowView (APIView) :
    permission_classes = [IsAuthenticated]

    def post (self, request, user_id) :
        header = JWTTokenUserAuthentication.get_header(self, request=request)
        raw_token = JWTTokenUserAuthentication.get_raw_token(self, header=header)
        user = CheckJWT.get_user(raw_token)

        following_user = User.objects.get(pk=user_id)

        serializer = FollowingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try :
            follow = Follow.objects.get(following_user_id=following_user, user_id=user)

        except Follow.DoesNotExist :
            if following_user != user :
                serializer.save(following_user_id=following_user, user_id=user)
                return Response({'success': '해당 유저를 팔로우 했습니다.'}, status=200)
            return Response({'detail': '자기 자신은 팔로우 할 수 없습니다.'}, status=400)

        return Response({'detail': '이미 팔로우 한 유저입니다.'}, status=400)

    def get (self, request, user_id) :
        header = JWTTokenUserAuthentication.get_header(self, request=request)
        raw_token = JWTTokenUserAuthentication.get_raw_token(self, header=header)
        user = CheckJWT.get_user(raw_token)
        following_user = User.objects.get(pk=user_id)

        try :
            follow = Follow.objects.get(following_user_id=following_user, user_id=user)

        except Follow.DoesNotExist :
            return Response({'detail': '팔로우하지 않음.'}, status=400)

        return Response({'success': '팔로우함.'}, status=200)

    
    def delete (self, request, user_id) :
        header = JWTTokenUserAuthentication.get_header(self, request=request)
        raw_token = JWTTokenUserAuthentication.get_raw_token(self, header=header)
        user = CheckJWT.get_user(raw_token)
        following_user = User.objects.get(pk=user_id)

        try :
            follow = Follow.objects.get(following_user_id=following_user, user_id=user)

        except Follow.DoesNotExist :
            return Response({'detail': '해당 유저를 팔로우 하지 않았습니다.'}, status=400)

        follow.delete()

        return Response({'success': '해당 유저를 언팔로우 하였습니다.'}, status=200)

class UsersPostView (ModelViewSet) :
    serializer_class = PostSerializer

    def get_queryset (self) :
        queryset = Post.objects.filter(owner=self.kwargs.get('user_id'))
        return queryset

class MyProfileView (ModelViewSet) :
    permission_classes = [IsAuthenticated]
    serializer_class = userProfileSerializer

    def list (self, request) :
        header = JWTTokenUserAuthentication.get_header(self, request=request)
        raw_token = JWTTokenUserAuthentication.get_raw_token(self, header=header)

        user = CheckJWT.get_user(raw_token)
        serializer = self.serializer_class(user)
        
        return Response(serializer.data)

class UserProfileView (ModelViewSet) :
    serializer_class = userProfileSerializer

    def list (self, request, *args, **kwargs) :
        queryset = User.objects.filter(id=kwargs.get('user_id'))
        serializer = self.serializer_class(queryset, context={'request': request})
        
        try :
            return Response(serializer.data[0])

        except IndexError :
            return Response({'message': ['존재하지 않는 유저입니다.']}, status=400)