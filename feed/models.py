from django.db import models
from django.conf import settings

class Post (models.Model) :
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author', null=True)
    title = models.CharField(max_length=40)
    content = models.TextField(max_length=300)
    tag = models.CharField(max_length=511, null=True)
    view_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__ (self) :
        return self.title

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
    created_at = models.DateTimeField(auto_now_add=True)

class Like (models.Model) :
    liked_people = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='liked_people', null=True)