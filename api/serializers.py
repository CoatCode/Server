from .models import User, Follow
from django.contrib import auth
from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime, timedelta

class customRegisterSerializer (serializers.ModelSerializer) :
    email = serializers.CharField(allow_null=True)
    password = serializers.CharField(max_length=999, min_length=8, write_only=True, allow_null=True)
    username = serializers.CharField(allow_null=True)
    image = serializers.ImageField(use_url=True, required=False)
    
    class Meta :
        model = User
        fields = ['email', 'username', 'image', 'password']

    def validate (self, attrs) :
        email = attrs.get('email', None)
        password = attrs.get('password', None)
        username = attrs.get('username', None)
        
        error = {}

        try :
            check_email = User.objects.get(email=email)
        except User.DoesNotExist :
            check_email = None
        
        try :
            check_username = User.objects.get(username=username)
        except User.DoesNotExist :
            check_username = None

        if check_email is not None and check_username is not None :
            error['message'] = '이미 존재하는 이메일과 이름 입니다.'
            raise serializers.ValidationError(error)

        if check_email is not None :
            error['message'] = '이미 존재하는 이메일 입니다.'
            raise serializers.ValidationError(error)

        if check_username is not None :
            error['message'] = '이미 존재하는 이름 입니다.'
            raise serializers.ValidationError(error)

        if email is None and password is None and username is None :
            error['message'] = '이메일, 비밀번호 그리고 이름을 입력해주세요'
            raise serializers.ValidationError(error)

        if email is None and password is None :
            error['message'] = '이메일과 비밀번호를 입력해주세요.'
            raise serializers.ValidationError(error)

        if email is None and username is None :
            error['message'] = '이메일과 이름 입력해주세요.'
            raise serializers.ValidationError(error)

        if email is None and password is None :
            error['message'] = '이메일과 비밀번호를 입력해주세요.'
            raise serializers.ValidationError(error)

        if email is None :
            error['message'] = '이메일을 입력해주세요.'
            raise serializers.ValidationError(error)

        if password is None :
            error['message'] = '비밀번호를 입력해주세요.'
            raise serializers.ValidationError(error)

        if username is None :
            error['message'] = '이름을 입력해주세요.'
            raise serializers.ValidationError(error)

        return attrs
        
    def create (self, validate_data) :
        image = validate_data.get('image', None)
        if image is None :
            validate_data.update({'image': 'media/main_profile_picture_ch8orj'})
        username = validate_data['username']
        validate_data.update({'description': F'안녕하세요. {username}입니다.'})
        return User.objects.create_user(**validate_data)

class customLoginSerializer (serializers.Serializer) :
    email = serializers.CharField(max_length=64)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate (self, attrs) :
        token = RefreshToken.for_user

        email = attrs.get('email', None)
        password = attrs.get('password', None)

        try :
            user = User.objects.get(email=email)

        except User.DoesNotExist :
            raise AuthenticationFailed('이메일 또는 비밀번호를 확인해주세요.')

        if user.check_password(raw_password=password) is False :
            up = password.upper()

            if user.check_password(raw_password=up) is False :
                down = up.lower()

                if user.check_password(raw_password=down) is False :
                    raise AuthenticationFailed('이메일 또는 비밀번호를 확인해주세요.')
        
        if user.is_verified is False :
            raise AuthenticationFailed('이메일 인증을 먼저 해주세요.')

        if user.is_active is False :
            raise AuthenticationFailed('관리자에게 문의해주세요.')

        return attrs

class customTokenRefreshSerializer (serializers.Serializer) :
    refresh = serializers.CharField(max_length=999)

class userProfileSerializer (serializers.ModelSerializer) :
    profile = serializers.ImageField(source='image')
    following = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    
    class Meta :
        model = User
        fields = ('id', 'email', 'username', 'profile', 'description', 'following', 'followers')

    def get_following (self, obj) :
        serializer = FollowingSerializer(obj.following.all(), many=True).data
        return len(serializer)

    def get_followers (self, obj) :
        serializer = FollowersSerializer(obj.followers.all(), many=True).data
        return len(serializer)

class FollowingSerializer (serializers.ModelSerializer) :

    class Meta :
        model = Follow
        fields = ("id", "following_user_id", "created")

class FollowersSerializer (serializers.ModelSerializer) :

    class Meta :
        model = Follow
        fields = ("id", "user_id", "created")