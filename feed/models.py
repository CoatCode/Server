from django.db import models
from django.conf import settings

class post (models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='authorName', null=True)
    title = models.CharField(max_length=40)
    text = models.TextField(max_length=300)
    image1 = models.ImageField(blank=True, null=True)
    image2 = models.ImageField(blank=True, null=True)
    image3 = models.ImageField(blank=True, null=True)
    image4 = models.ImageField(blank=True, null=True)
    image5 = models.ImageField(blank=True, null=True)
    view = models.IntegerField(default=0)
    like = models.IntegerField(default=0)
    liker = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liker', blank=True)
    tag1 = models.CharField(max_length=20, null=True)
    tag2 = models.CharField(max_length=20, null=True)
    tag3 = models.CharField(max_length=20, null=True)
    tag4 = models.CharField(max_length=20, null=True)
    tag5 = models.CharField(max_length=20, null=True)

class comment (models.Model) :
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(post, on_delete=models.CASCADE)
    text = models.TextField(max_length=200)