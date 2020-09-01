from rest_framework import serializers
from .models import post, comment

class commentSerializer (serializers.ModelSerializer) :
    author = serializers.CharField(source='author.username', read_only=True)
    
    class Meta :
        model = comment
        fields = ['author', 'text']

class postSerializer (serializers.ModelSerializer) :
    author = serializers.CharField(source='author.username', read_only=True)
    image1 = serializers.ImageField(use_url=True, allow_null=True)
    image2 = serializers.ImageField(use_url=True, allow_null=True)
    image3 = serializers.ImageField(use_url=True, allow_null=True)
    image4 = serializers.ImageField(use_url=True, allow_null=True)
    image5 = serializers.ImageField(use_url=True, allow_null=True)
    comment = commentSerializer(many=True, read_only=True)

    class Meta:
        model = post
        fields = ['pk', 'author', 'title', 'text', 'image1', 'image2', 'image3', 'image4', 'image5', 'like', 'liker', 'tag1', 'tag2', 'tag3', 'tag4', 'tag5', 'comment', 'view']

    def create (self, validated_data) :
        return post.objects.create(**validated_data)