from rest_framework import serializers
from .models import Post, Comment, Image
from api.models import User

class AuthorSerializer(serializers.ModelSerializer):
    profile = serializers.ImageField(use_url=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'profile']

class ImageSerializer (serializers.ModelSerializer) :
    image = serializers.ImageField(use_url=True)

    class Meta :
        model = Image
        fields = ['image']

class CommentSerializer (serializers.ModelSerializer) :
    author = AuthorSerializer(read_only=True)
    
    class Meta:
        model = Comment
        fields = ['pk', 'author', 'text', 'created_at']

class PostSerializer (serializers.ModelSerializer) :
    author = AuthorSerializer(read_only=True)
    title = serializers.CharField(allow_null=True)
    text = serializers.CharField(allow_null=True)
    image = ImageSerializer(read_only=True)
    like_cnt = serializers.IntegerField(source='liker.count', read_only=True)
    comment_cnt = serializers.ReadOnlyField()

    class Meta:
        model = Post
        fields = ['pk', 'author', 'title', 'text', 'image', 'view', 'like_cnt', 'comments', 'comment_cnt', 'liker', 'tag', 'created_at']

    def create (self, validated_data) :
        images_data = self.context['request'].FILES
        post = Post.objects.create(**validated_data)

        for image_data in images_data.getlist('image') :
            Image.objects.create(post=post, image=image_data)

        return post