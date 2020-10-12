from rest_framework import serializers
from .models import Post, Comment, Image, Like
from api.serializers import userProfileSerializer, FollowingSerializer, FollowersSerializer
from api.models import User, Follow
from django.shortcuts import get_object_or_404

class ImageSerializer (serializers.ModelSerializer) :
    image = serializers.ImageField(use_url=True)

    class Meta :
        model = Image
        fields = ('image', )

class CommentSerializer (serializers.ModelSerializer) :
    comment_id = serializers.IntegerField(source='id')
    owner = userProfileSerializer(read_only=True)

    class Meta :
        model = Comment
        fields = ('comment_id', 'owner', 'content', 'created_at')

    def create (self, validated_data) :
        return Comment.objects.create(**validated_data)

    def validate (self, attrs) :
        text = attrs.get('text', '')

        error = {}

        if text is None :
            error['message'] = '본문은 빈칸일 수 없습니다.'
            raise serializers.ValidationError(error)

        return attrs

class LikeSerializer (serializers.ModelSerializer) :

    class Meta :
        model = Like
        fields = '__all__'

class PostSerializer (serializers.ModelSerializer) :
    owner = userProfileSerializer(read_only=True)
    like_count = serializers.ReadOnlyField()
    comment_count = serializers.ReadOnlyField()
    images = ImageSerializer(read_only=True, many=True)
    liked_people = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta :
        model = Post
        fields = ('id', 'owner', 'title', 'content', 'view_count', 'images', 'like_count', 'comment_count', 'liked_people', 'tag', 'created_at')

    def create (self, validated_data) :
        images_data = self.context['request'].FILES
        post = Post.objects.create(**validated_data)
        
        for i in range(1, 6) :
            image_data = images_data.get(F'image{i}')

            if image_data is None :
                break

            Image.objects.create(post=post, image=image_data)

        return post

    def to_representation (self, instance) :
        data = super().to_representation(instance)
        images = data.pop('images')
        images_array = [a.get('image') for a in images]
        data.update({'image_url': images_array})
        return data

    def validate (self, attrs) :
        title = attrs.get('title', '')
        content = attrs.get('text', '')

        error = {}

        if title is None and content is None :
            error['message'] = '제목과 본문은 빈칸일 수 없습니다.'
            raise serializers.ValidationError(error)

        if title is None :
            error['message'] = '제목은 빈칸일 수 없습니다.'
            raise serializer.ValidationError(error)

        if content is None :
            error['message'] = '본문은 빈칸일 수 없습니다.'    
            raise serializer.ValidationError(error)

        return attrs