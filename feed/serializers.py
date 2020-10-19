from rest_framework import serializers
from .models import Post, Comment, Image, Like
from api.serializers import userProfileSerializer, FollowingSerializer, FollowersSerializer
from api.models import User, Follow
from datetime import datetime
import random

class ImageSerializer (serializers.ModelSerializer) :
    image = serializers.ImageField(use_url=True)

    class Meta :
        model = Image
        fields = ('image', )

class CommentSerializer (serializers.ModelSerializer) :
    comment_id = serializers.IntegerField(source='id', read_only=True)
    owner = userProfileSerializer(read_only=True)

    class Meta :
        model = Comment
        fields = ('comment_id', 'owner', 'content', 'created_at')

    def create (self, validated_data) :
        return Comment.objects.create(**validated_data, created_at=str(datetime.now().astimezone().replace(microsecond=0).isoformat()))

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

    def create (self, validated_data) :
        return Like.objects.create(**validated_data)

class PostSerializer (serializers.ModelSerializer) :
    owner = userProfileSerializer(read_only=True)
    like_count = serializers.ReadOnlyField()
    comment_count = serializers.ReadOnlyField()
    images = ImageSerializer(read_only=True, many=True)
    liked_people = LikeSerializer(many=True, read_only=True)
    tag = serializers.ListField(child=serializers.CharField())
    comments = CommentSerializer(many=True, read_only=True)

    class Meta :
        model = Post
        fields = ('id', 'owner', 'title', 'content', 'view_count', 'images', 'like_count', 'comment_count', 'liked_people', 'tag', 'created_at', 'comments')

    def create (self, validated_data) :
        images_data = self.context['request'].FILES
        post = Post.objects.create(**validated_data, created_at=str(datetime.now().astimezone().replace(microsecond=0).isoformat()))
        
        for i in range(1, 6) :
            image_data = images_data.get(F'image{i}')

            if image_data is None :
                break

            Image.objects.create(post=post, image=image_data)

        return post

    def to_representation (self, instance) :
        data = super().to_representation(instance)
        images = data.pop('images')
        liked_people = data.pop('liked_people')
        comments = data.pop('comments')
        images_array = [image.get('image') for image in images]
        liked_people_array = [liked_person.get('liked_people') for liked_person in liked_people]
        comments_array = [comment for comment in comments]

        if comments_array != [] :
            if len(comments_array) == 1 or len(comments_array) == 2:
                data.update({'image_urls': images_array, 'liked_people': liked_people_array, 'comments_preview': comments_array})

            else :
                comments_preview_array = []

                for i in range(2) :
                    random_comment = random.choice(comments_array)
                    comments_array.remove(random_comment)
                    comments_preview_array.append(random_comment)

                data.update({'image_urls': images_array, 'liked_people': liked_people_array, 'comments_preview': comments_preview_array})
                    
        else :
            data.update({'image_urls': images_array, 'liked_people': liked_people_array})

        return data

    def validate (self, attrs) :
        title = attrs.get('title', '')
        content = attrs.get('text', '')
        tag = attrs.get('tag', '')

        error = {}

        if title is None and content is None :
            error['message'] = '제목과 본문은 빈칸일 수 없습니다.'
            raise serializers.ValidationError(error)

        if title is None :
            error['message'] = '제목은 빈칸일 수 없습니다.'
            raise serializers.ValidationError(error)

        if content is None :
            error['message'] = '본문은 빈칸일 수 없습니다.'    
            raise serializers.ValidationError(error)

        return attrs