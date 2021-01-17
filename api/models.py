from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, PermissionsMixin)
from django.db import models
from django.utils import timezone
from datetime import datetime
import uuid

class UserManager (BaseUserManager) :
    
    def create_user (self, username, email, image, description, password=None) :

        if username is None :
            raise TypeError('Users should have a username')

        if email is None :
            raise TypeError('Users should have a email')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            image=image,
            description=description
        )
        
        user.set_password(password)
        user.save()
        
        return user

    def create_superuser (self, username, email, image, password=None) :

        if password is None :
            raise TypeError('Password should not be none')

        user = self.create_user(
            username,
            email,
            image,
            password,
            description,
        )
        
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user

class User (AbstractBaseUser, PermissionsMixin) :
    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.CharField(max_length=255, unique=True, db_index=True)
    image = models.ImageField(blank=True, null=True)
    description = models.CharField(max_length=255, null=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    refresh_token_expires_at = models.CharField(default='0', max_length=255)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'image', 'description']

    objects = UserManager()

    def __str__ (self) :
        return self.email
        
class Follow (models.Model) :
    user = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE, null=True)
    following_user = models.ForeignKey(User, related_name="followers", on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta :
        unique_together = ("user_id", "following_user_id")
        ordering = ["-created"]