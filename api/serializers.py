from .models import User
from django.contrib import auth
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib import auth
from django.utils.translation import ugettext_lazy as _
from datetime import datetime, timedelta

class Base64ImageField (serializers.ImageField) :

    def to_internal_value (self, data) :
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        if isinstance(data, six.string_types):
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
    password = serializers.CharField(max_length=999, min_length=8, write_only=True)
    profile = Base64ImageField(use_url=True, allow_null=True)
    
    class Meta :
        model = User
        fields = ['email', 'username', 'profile', 'password']

    def validate (self, attrs) :
        email = attrs.get('email', '')
        username = attrs.get('username', '')
        profile = attrs.get('profile', '')

        return attrs
        
    def create (self, validate_data) :
        return User.objects.create_user(**validate_data)

class customLoginSerializer (serializers.ModelSerializer) :
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=999, min_length=8, write_only=True)

    class Meta :
        model = User
        fields = ['email', 'password']

    def validate (self, attrs) :
        email = attrs.get('email', '')

        return attrs

class customTokenRefreshSerializer (TokenRefreshSerializer) :

    def validate (self, attrs) :
        data = super().validate(attrs)
        refresh = RefreshToken(attrs['refresh'])

        data['token_type'] = 'Bearer'
        data['access_token'] = str(refresh.access_token)
        data['expires_at'] = str(datetime.now() + timedelta(minutes=30))
        data['refresh_token'] = str(refresh)
        data['refresh_token_expires_at'] = str(datetime.now() + timedelta(hours=8))
        
        del(data['access'])

        return data

class userProfileSerializer (serializers.ModelSerializer) :
    profile = Base64ImageField(use_url=True)
    
    class Meta :
        model = User
        fields = ('email', 'username', 'profile')