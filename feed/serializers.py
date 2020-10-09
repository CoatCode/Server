from rest_framework import serializers
from .models import Post, Comment, Image, Like
from api.models import User

class AuthorSerializer (serializers.ModelSerializer) :
    profile = serializers.ImageField(use_url=True)

    class Meta :
        model = User
        fields = ('username', 'email', 'profile')

class ImageSerializer (serializers.ModelSerializer) :
    image = serializers.ImageField(use_url=True)

    class Meta :
        model = Image
        fields = ('image', )

class CommentSerializer (serializers.ModelSerializer) :
    author = AuthorSerializer(read_only=True)
    
    class Meta :
        model = Comment
        fields = ('pk', 'author', 'text', 'created_at')

    def create (self, validated_data) :
        return Comment.objects.create(**validated_data)

    def validate (self, attrs) :
        text = attrs.get('text', '')

        error ={}

        if text is None :
            error['message'] = '본문은 빈칸일 수 없습니다.'
            serializers.ValidationError(error)

        return attrs

class LikeSerializer (serializers.ModelSerializer) :
    id = serializers.CharField(source='liker.pk')
    email = serializers.CharField(source='liker.email')
    username = serializers.CharField(source='liker.username')
    profile = serializers.ImageField(use_url=True, source='liker.profile')

    class Meta :
        model = Like
        fields = ('id', 'email', 'username', 'profile')

class LikerSerializer (serializers.ModelSerializer) :
    id = serializers.IntegerField(source='liker.pk')

    class Meta :
        model = Like
        fields = ('id', )

class PostSerializer (serializers.ModelSerializer) :
    author = AuthorSerializer(read_only=True)
    image = ImageSerializer(many=True, required=False, read_only=True)
    liker = LikerSerializer(many=True, required=False)
    like_count = serializers.ReadOnlyField()
    comment_count = serializers.ReadOnlyField()

    class Meta :
        model = Post
        fields = ('pk', 'author', 'title', 'text', 'view', 'image', 'like_count', 'liker', 'comment_count', 'tag', 'created_at')
 
    def create (self, validated_data) :
        images_data = self.context['request'].FILES
        post = Post.objects.create(**validated_data)

        for image_data in images_data.getlist('image') :
            Image.objects.create(post=post, image=image_data)

        return post

    def validate (self, attrs) :
        title = attrs.get('title', '')
        text = attrs.get('text', '')

        error = {}

        if title is None and text is None :
            error['message'] = '제목과 본문은 빈칸일 수 없습니다.'
            serializers.ValidationError(error)

        if title is None :
            error['message'] = '제목은 빈칸일 수 없습니다.'
            serializer.ValidationError(error)

        if text is None :
            error['message'] = '본문은 빈칸일 수 없습니다.'    
            serializer.ValidationError(error)

        return attrs