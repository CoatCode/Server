from .models import Post, Comment, Image, Like
from api.models import User
from .serializers import PostSerializer, CommentSerializer, LikeSerializer, LikerSerializer
from .permissions import IsAuthor
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

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
        serializer.save(author=self.request.user)

    def create (self, request, *args, **kwargs) :
        super().create(request, *args, **kwargs)
        return Response({'success': '게시물이 저장 되었습니다.'}, status=201)

class UpdateDeletePostView (ModelViewSet) :
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsAuthor]
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
        serializer.save(author=self.request.user, post=post)

    def get_queryset (self) :
        return super().get_queryset().filter(post=self.kwargs.get('post_id'))

    def create (self, request, *args, **kwargs) :
        super().create(request, *args, **kwargs)
        return Response({'success': '댓글이 저장 되었습니다.'}, status=201)

class UpdateDeleteCommentView (ModelViewSet) :
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthor]
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

    def get_queryset (self) :
        return super().get_queryset().filter(post=self.kwargs.get('post_id'))

    def perform_create (self, serializer) :
        postId = self.kwargs.get('post_id')
        post = Post.objects.get(pk=postId)
        serializer.save(author=self.request.user, post=post)

    def create (self, request, *args, **kwargs) :
        super().create(request, *args, **kwargs)
        return Response({'success': '해당 게시물을 좋아요 했습니다.'}, status=200)

class GetLikeUnlikeView (ModelViewSet) :
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset (self) :
        return super().get_queryset().filter(post=self.kwargs.get('post_id'))

    def list (self, request, *args, **kwargs) :
        super().list(request, *args, **kwargs)

        try :
            like = Like.objects.get(liker=self.request.user)

        except like.DoesNotExist :
            return Response({'message': ['좋아요 하지 않음.']}, status=400)

        return Response({'success': '좋아요함'}, status=200)

class DeleteLikeView (ModelViewSet) :
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated, IsAuthor]

    def get_queryset (self) :
        return super().get_queryset().filter(post=self.kwargs.get('post_id'))

    def destroy (self, request, *args, **kwargs) :
        super().destroy(request, *args, **kwargs)
        return Response({'success': '해당 게시물의 좋아요를 취소했습니다.'}, status=200)