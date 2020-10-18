from .models import User, Follow
from feed.models import Post
from .permissions import IsFollower
from .utils import Util
from .serializers import customRegisterSerializer, customLoginSerializer, customTokenRefreshSerializer, userProfileSerializer, FollowersSerializer, FollowingSerializer
from feed.serializers import PostSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.urls import reverse
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

        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(request).domain
        relativeLink = reverse('emailVerify')
        
        absurls = F'http://{current_site}{relativeLink}?token={token}'
        email_body = F'Hi {user.username} Use link below to verify your email \n{absurls}'
        data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'Verify your email'}
        Util.send_email(data)
        
        return Response({'message': '이메일을 확인하세요.'}, status=201)

class customLoginView (GenericAPIView) :
    serializer_class = customLoginSerializer

    def post (self, request) :
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try :
            user = User.objects.get(email=serializer.data['email'])

        except User.DoesNotExist :
            return Response({'message': ['이메일 또는 비밀번호를 확인해주세요.']}, status=401)

        if user.check_password(raw_password=serializer.data['password']) == False :
            up = serializer.data['password'].upper()

            if user.check_password(raw_password=up) == False :
                down=serializer.data['password'].lower()
                
                if user.check_password(raw_password=down) == False :
                    return Response({'message': ['이메일 또는 비밀번호를 확인해주세요.']}, status=401)

        if not user.is_verified :
            return Response({'message': ['이메일 인증을 먼저 해주세요.']}, status=401)

        if not user.is_active :
            return Response({'message': ['계정이 비활성화 되었습니다. 관리자에게 문의하세요.']}, status=401)

        token = RefreshToken.for_user(user)

        data = {
            'token_type': 'Bearer',
            'access_token': str(token.access_token),
            'expires_at': str((datetime.now() + timedelta(minutes=30)).astimezone().replace(microsecond=0).isoformat()),
            'refresh_token': str(token),
            'refresh_token_expires_at': str((datetime.now() + timedelta(hours=8)).astimezone().replace(microsecond=0).isoformat())
        }

        return Response(data, status=200)

class customRefreshView (GenericAPIView) :
    serializer_class = customTokenRefreshSerializer

    def post (self, request) :
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try :
            token = RefreshToken(serializer.data['refresh'])

        except :
            return Response({'message': ['잘못된 refresh token 입니다.']}, status=401)

        data = {
            'token_type': 'Bearer',
            'access_token': str(token.access_token),
            'expires_at': str((datetime.now() + timedelta(minutes=30)).astimezone().replace(microsecond=0).isoformat()),
            'refresh_token': str(token),
            'refresh_token_expires_at': str((datetime.now() + timedelta(hours=8)).astimezone().replace(microsecond=0).isoformat())
        }

        return Response(data, status=200)

class VerifyEmail (GenericAPIView) :

    def get (self, request) :
        token = request.GET.get('token')

        try :
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified :
                user.is_verified = True
                user.save()
            return Response({'success': '성공적으로 인증되었습니다'})

        except jwt.ExpiredSignatureError :
            return Response({'message': ['인증이 만료되었습니다']}, status=400)
        
        except jwt.exceptions.DecodeError :
            return Response({'message': ['잘못된 토큰입니다']}, status=400)

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

class UserUnfollowingView (ModelViewSet) :
    permission_classes = [IsAuthenticated, IsFollower]
    serializer_class = FollowingSerializer
    queryset = Follow.objects.all()

    def get_queryset (self) :
        return super().get_queryset().filter(following_user_id=self.kwargs.get('user_id'))

    def destroy (self, request, *args, **kwargs) :
        super().destroy(request, *args, **kwargs)
        return Response({'success': '해당 사용자를 언팔로우 했습니다.'}, status=200)

class FollowView (APIView) :
    permission_classes = [IsAuthenticated]

    def post (self, request, user_id) :
        user = User.objects.get(pk=user_id)
        serializer = FollowingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try :
            follow = Follow.objects.get(following_user_id=user, user_id=self.request.user)

        except Follow.DoesNotExist :
            if user != self.request.user :
                serializer.save(following_user_id=user, user_id=self.request.user)
                return Response({'success': '해당 유저를 팔로우 했습니다.'}, status=200)
            return Response({'message': ['자기 자신은 팔로우할 수 없습니다.']}, status=200)

        return Response({'message': ['이미 팔로우 한 유저입니다.']}, status=400)

    def get (self, request, user_id) :
        user = User.objects.get(pk=user_id)

        try :
            follow = Follow.objects.get(following_user_id=user, user_id=self.request.user)

        except Follow.DoesNotExist :
            return Response({'message': ['팔로우하지 않음.']}, status=200)

        return Response({'success': '팔로우함.'}, status=400)

    
    def delete (self, request, user_id) :
        user = User.objects.get(pk=user_id)

        try :
            follow = Follow.objects.get(following_user_id=user, user_id=self.request.user)

        except Follow.DoesNotExist :
            return Response({'message': ['해당 유저를 팔로우 하지 않았습니다.']}, status=200)

        follow.delete()

        return Response({'success': '해당 유저를 언팔로우 하였습니다.'}, status=200)

class UsersPostView (ModelViewSet) :
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def get_queryset (self) :
        queryset = Post.objects.filter(owner=self.kwargs.get('user_id'))
        return queryset

class MyProfileView (ModelViewSet) :
    permission_classes = [IsAuthenticated]
    serializer_class = userProfileSerializer

    def list (self, request) :
        queryset = User.objects.filter(email=self.request.user)
        serializer = self.serializer_class(queryset, many=True)

        for i in serializer.data :
            data = i

        return Response(data)

class UserProfileView (ModelViewSet) :
    permission_classes = [IsAuthenticated]
    serializer_class = userProfileSerializer

    def list (self, request) :
        queryset = User.objects.filter(id=self.kwargs.get('user_id'))
        serializer = self.serializer_class(queryset, many=True)

        for i in serializer.data :
            data = i
        
        return Response(data)