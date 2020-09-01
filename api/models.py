from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, PermissionsMixin)
from django.db import models
from django.utils import timezone

class UserManager (BaseUserManager) :
    
    def create_user (self, username, email, profile, password=None) :

        if username is None :
            raise TypeError('Users should have a username')

        if email is None :
            raise TypeError('Users should have a email')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            profile=profile,
        )
        
        user.set_password(password)
        user.save()
        
        return user

    def create_superuser (self, username, email, profile, password=None) :

        if password is None :
            raise TypeError('Password should not be none')

        user = self.create_user(
            username,
            email,
            profile,
            password
        )
        
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user

class User (AbstractBaseUser, PermissionsMixin) :
    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.CharField(max_length=255, unique=True, db_index=True)
    profile = models.ImageField(default='media\default_image.jpeg', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'profile']

    objects = UserManager()

    def __str__ (self) :
        return self.email