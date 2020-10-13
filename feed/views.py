from .models import Post, Comment, Image, Like
from api.models import User
from api.serializers import userProfileSerializer
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from .permissions import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.http import HttpResponseRedirect

class LargeResultsSetPagination (PageNumberPagination) :
    page_size = 15
    page_query_param = 'page'
    max_page_size = 100

    def get_paginated_response (self, data) :
        return Response(data)

class CreateReadPostView (ModelViewSet) :
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    pagination_class = LargeResultsSetPagination

    def perform_create (self, serializer) :
        serializer.save(owner=self.request.user)

    def create (self, request, *args, **kwargs) :
        super().create(request, *args, **kwargs)
        return Response({'success': '게시물이 저장 되었습니다.'}, status=201)

class UpdateDeletePostView (ModelViewSet) :
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = Post.objects.all()

    def update (self, request, *args, **kwargs) :
        super().update(request, *args, **kwargs)
        return Response({'success': '게시물이 수정 되었습니다.'}, status=200)

    def destroy (self, request, *args, **kwargs) :
        super().destroy(request, *args, **kwargs)
        return Response({'success': '게시물이 삭제 되었습니다.'}, status=200)

class CreateReadCommentView (ModelViewSet) :
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()

    def perform_create (self, serializer) :
        postId = self.kwargs.get('post_id')
        post = Post.objects.get(pk=postId)
        serializer.save(owner=self.request.user, post=post)

    def get_queryset (self) :
        return super().get_queryset().filter(post=self.kwargs.get('post_id'))

    def create (self, request, *args, **kwargs) :
        super().create(request, *args, **kwargs)
        return Response({'success': '댓글이 저장 되었습니다.'}, status=201)

class UpdateDeleteCommentView (ModelViewSet) :
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = Comment.objects.all()

    def get_queryset (self) :
        return super().get_queryset().filter(post=self.kwargs.get('post_id'))

    def update (self, request, *args, **kwargs) :
        super().update(request, *args, **kwargs)
        return Response({'success': '댓글이 수정 되었습니다.'}, status=200)

    def destroy (self, request, *args, **kwargs) :
        super().destroy(request, *args, **kwargs)
        return Response({'success': '댓글이 삭제 되었습니다.'}, status=200)

class CreateReadLikeView (ModelViewSet) :
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]
    queryset = Like.objects.all()
    is_saved = False

    def get_queryset (self) :
        return super().get_queryset().filter(post=self.kwargs.get('post_id'))

    def perform_create (self, serializer) :
        postId = self.kwargs.get('post_id')
        post = Post.objects.get(pk=postId)

        try :
            like = self.queryset.get(post=post, liked_people=self.request.user)

        except Like.DoesNotExist :
            serializer.save(liked_people=self.request.user, post=post)
            self.is_saved = True

    def create (self, request, *args, **kwargs) :
        super().create(request, *args, **kwargs)
        
        if self.is_saved is True :
            self.is_saved = False
            return Response({'success': '해당 게시물을 좋아요 했습니다.'}, status=200)

        return Response({'message': ['이미 해당 게시물을 좋아요 하였습니다.']}, status=400)

    def list (self, request, *args, **kwargs) :
        postId = self.kwargs.get('post_id')
        post = Post.objects.get(pk=postId)

        try :
            like = self.queryset.get(post=post, liked_people=self.request.user)

        except Like.DoesNotExist :
            return Response({'message': ['좋아요 하지 않음.']}, status=400)

        return Response({'success': '좋아요함.'}, status=200)

class ReadLikerView (ModelViewSet) :
    serializer_class = userProfileSerializer
    permission_classes = [IsAuthenticated]
    queryset = Like.objects.all()

    def get_queryset (self) :
        return super().get_queryset().filter(post=self.kwargs.get('post_id'))

    def list (self, request, *args, **kwargs) :
        likers = self.queryset.filter(post=self.kwargs.get('post_id')).values()
        data = []

        for liker in likers :
            userId = liker.get('liked_people_id')
            user = User.objects.filter(pk=userId)
            serializer = self.serializer_class(user, many=True)
            data.append(serializer.data[0])

        return Response(data)

class DeleteLikeView (ModelViewSet) :
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated, IsLiker]
    queryset = Like.objects.all()

    def get_queryset (self) :
        return super().get_queryset().filter(post=self.kwargs.get('post_id'))

    def destroy (self, request, *args, **kwargs) :
        super().destroy(request, *args, **kwargs)
        return Response({'success': '해당 게시물의 좋아요를 취소했습니다.'}, status=200)