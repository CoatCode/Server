from .models import User, Follow
from django.contrib import auth
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import ugettext_lazy as _
from datetime import datetime, timedelta

class Base64ImageField (serializers.ImageField) :

    def to_internal_value (self, data) :
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        if isinstance (data, six.string_types) :
            if 'data:' in data and ';base64,' in data:
                header, data = data.split(';base64,')

            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            file_name = str(uuid.uuid4())[:12]
            file_extension = self.get_file_extension(file_name, decoded_file)
            complete_file_name = "%s.%s" % (file_name, file_extension, )
            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension (self, file_name, decoded_file) :
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension

class customRegisterSerializer (serializers.ModelSerializer) :
    email = serializers.CharField(allow_null=True)
    password = serializers.CharField(max_length=999, min_length=8, write_only=True, allow_null=True)
    username = serializers.CharField(allow_null=True)
    profile = Base64ImageField(allow_null=True, use_url=True)
    
    class Meta :
        model = User
        fields = ['email', 'username', 'profile', 'password']

    def validate (self, attrs) :
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        username = attrs.get('username', '')
        
        error = {}

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
        return User.objects.create_user(**validate_data)

class customLoginSerializer (serializers.ModelSerializer) :
    email = serializers.CharField(allow_null=True)
    password = serializers.CharField(max_length=999, allow_null=True)

    class Meta :
        model = User
        fields = ['email', 'password']

    def validate (self, attrs) :
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        if email is None and password is None :
            error['message'] = '이메일과 비밀번호를 입력해주세요.'
            raise serializers.ValidationError(error)

        if email is None :
            error['message'] = '이메일을 입력해주세요.'
            raise serializers.ValidationError(error)

        if password is None :
            error['message'] = '비밀번호를 입력해주세요.'
            raise serializers.ValidationError(error)

        return attrs

class customTokenRefreshSerializer (serializers.Serializer) :
    refresh = serializers.CharField(max_length=999)

    def validate (self, attrs) :
        refreshToken = attrs.get('refresh', '')

        return attrs

class userProfileSerializer (serializers.ModelSerializer) :
    profile = serializers.ImageField(use_url=True)
    following = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    
    class Meta :
        model = User
        fields = ['id', 'email', 'username', 'profile', 'following', 'followers']

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