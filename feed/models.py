from django.db import models
from django.conf import settings

class Post (models.Model) :
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author', null=True)
    title = models.CharField(max_length=40, null=True)
    text = models.TextField(max_length=300, null=True)
    tag = models.CharField(max_length=511, null=True)
    view = models.IntegerField(default=0)
    liker = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liker', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__ (self) :
        return self.title

    @property
    def comment_count (self) :
        return Comment.objects.filter(post=self.pk).count()        

class Image (models.Model) :
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)

class Comment (models.Model) :
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)