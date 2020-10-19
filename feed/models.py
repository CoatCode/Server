from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField

class Post (models.Model) :
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author', null=True)
    title = models.CharField(max_length=40)
    content = models.TextField(max_length=300)
    tag = ArrayField(models.CharField(max_length=255), null=True)
    view_count = models.IntegerField(default=0)
    created_at = models.CharField(max_length=60, null=True)

    @property
    def comment_count (self) :
        return Comment.objects.filter(post=self.pk).count()

    @property
    def like_count (self) :
        return Like.objects.filter(post=self.pk).count()
 
class Image (models.Model) :
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(null=True, blank=True)

class Comment (models.Model) :
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owner', null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', null=True)
    content = models.TextField(max_length=200)
    created_at = models.CharField(max_length=60, null=True)

class Like (models.Model) :
    liked_people = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='liked_people', null=True)