from .models import Post, Comment, Image, Like
from api.models import User, Follow
from api.serializers import userProfileSerializer
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from .permissions import *
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from django.db.models import Count

class LargeResultsSetPagination (PageNumberPagination) :
    page_size = 15
    page_query_param = 'page'
    max_page_size = 100

    def get_paginated_response (self, data) :
        return Response(data)

class CreatePostView (ModelViewSet) :
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()

    def get_serializer_context (self) :
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def perform_create (self, serializer) :
        user = User.objects.get(email=self.request.user)
        serializer.save(owner=user)

    def create (self, request, *args, **kwargs) :
        super().create(request, *args, **kwargs)
        return Response({'success': '게시물이 저장 되었습니다.'}, status=201)

class ReadAllListPostView (ModelViewSet) :
    serializer_class = PostSerializer
    queryset = Post.objects.all().order_by('-pk')
    pagination_class = LargeResultsSetPagination

    def get_serializer_context (self) :
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class ReadPopularListPostView (ModelViewSet) :
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    pagination_class = LargeResultsSetPagination

    def list (self, request, *args, **kwargs) :
        post = self.queryset.annotate(number_of_likes=Count('liked_people')).order_by('-number_of_likes')
        serializer = self.serializer_class(post, many=True, context={'request': request})
        return Response(serializer.data)

class ReadFollowingPostView (ModelViewSet) :
    serializer_class = PostSerializer
    queryset = Post.objects.all().order_by('-pk')
    permission_classes = [IsAuthenticated]
    pagination_class = LargeResultsSetPagination

    def list (self, request, *args, **kwargs) :
        data = []
        followings = Follow.objects.filter(user_id=self.request.user)

        for following in followings :
            post = self.queryset.filter(owner=following.following_user_id)
            serializers = self.serializer_class(post, many=True, context={'request': request})
            
            for serializer in serializers.data :
                data.append(serializer)

        return Response(data)

class ReadOneUpdateDeletePostView (ModelViewSet) :
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Post.objects.all()

    def get_serializer_context (self) :
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def update (self, request, *args, **kwargs) :
        super().update(request, *args, **kwargs)
        return Response({'success': '게시물이 수정 되었습니다.'}, status=200)

    def destroy (self, request, *args, **kwargs) :
        super().destroy(request, *args, **kwargs)
        return Response({'success': '게시물이 삭제 되었습니다.'}, status=200)

class CreateCommentView (ModelViewSet) :
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()

    def get_serializer_context (self) :
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def perform_create (self, serializer) :
        postId = self.kwargs.get('post_id')
        post = Post.objects.get(pk=postId)
        user = User.objects.get(email=self.request.user)
        serializer.save(owner=user, post=post)

    def get_queryset (self) :
        return super().get_queryset().filter(post=self.kwargs.get('post_id'))

    def create (self, request, *args, **kwargs) :
        super().create(request, *args, **kwargs)
        return Response({'success': '댓글 작성이 완료되었습니다.'}, status=201)

class ReadCommentView (ModelViewSet) :
    serializer_class = CommentSerializer
    queryset = Comment.objects.all().order_by('pk')

    def list (self, request, *args, **kwargs) :
        postId = self.kwargs.get('post_id')
        post = Post.objects.get(pk=postId)
        post.view_count = post.view_count + 1
        post.save(update_fields=('view_count', ))

        comments = self.queryset.filter(post=postId)
        serializer = self.serializer_class(comments, many=True, context={'request': request})
        
        return Response(serializer.data)

class UpdateDeleteCommentView (ModelViewSet) :
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = Comment.objects.all()

    def get_serializer_context (self) :
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_queryset (self) :
        return super().get_queryset().filter(post=self.kwargs.get('post_id'))

    def update (self, request, *args, **kwargs) :
        super().update(request, *args, **kwargs)
        return Response({'success': '댓글 수정이 완료되었습니다.'}, status=200)

    def destroy (self, request, *args, **kwargs) :
        super().destroy(request, *args, **kwargs)
        return Response({'success': '댓글이 삭제 되었습니다.'}, status=200)

class ReadLikerView (ModelViewSet) :
    serializer_class = userProfileSerializer
    queryset = Like.objects.all()

    def get_queryset (self) :
        return super().get_queryset().filter(post=self.kwargs.get('post_id'))

    def list (self, request, *args, **kwargs) :
        likers = self.queryset.filter(post=self.kwargs.get('post_id')).values()
        data = []

        for liker in likers :
            userId = liker.get('liked_people_id')
            user = User.objects.filter(pk=userId).order_by('pk')
            serializer = self.serializer_class(user, many=True, context={'request': request})
            
            if serializer.data != [] :
                data.append(serializer.data[0])

        return Response(data)

class LikeView (APIView) :
    permission_classes = [IsAuthenticated]

    def post (self, request, post_id) :
        post = Post.objects.get(pk=post_id)
        serializer = LikeSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(email=self.request.user)

        try :
            like = Like.objects.get(post=post, liked_people=user)

        except Like.DoesNotExist :
            serializer.save(liked_people=user, post=post)
            return Response({'success': '해당 게시글에 좋아요를 눌렀습니다.'}, status=200)

        return Response({'detail': '이미 좋아요를 누른 게시물 입니다.'}, status=400)

    def get (self, request, post_id) :
        post = Post.objects.get(pk=post_id)
        user = User.objects.get(email=self.request.user)

        try :
            like = Like.objects.get(post=post, liked_people=user)

        except Like.DoesNotExist :
            return Response({'detail': '좋아요 하지 않음.'}, status=400)

        return Response({'success': '좋아요함'}, status=200)
    
    def delete (self, request, post_id) :
        post = Post.objects.get(pk=post_id)
        user = User.objects.get(email=self.request.user)

        try :
            like = Like.objects.get(post=post, liked_people=user)

        except Like.DoesNotExist :
            return Response({'detail': '해당 게시글에 좋아요 되어 있지 않습니다.'}, status=400)

        like.delete()

        return Response({'success': '해당 게시글에 대한 좋아요가 취소 되었습니다.'}, status=200) 