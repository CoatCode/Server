from .models import Post, Comment, Image
from api.models import User
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsAuthor
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

class LargeResultsSetPagination(PageNumberPagination):
    page_size = 15
    page_query_param = 'page'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response(data)

class CreateReadPostView (ModelViewSet) :
    lookup_field = 'title'
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    pagination_class = LargeResultsSetPagination

    def perform_create (self, serializer) :
        serializer.save(author=self.request.user)

class UpdateDeletePostView (ModelViewSet) :
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsAuthor]
    queryset = Post.objects.all()

# class CreateReadCommentView (ModelViewSet) :
#     serializer_class = CommentSerializer
#     permission_classes = [IsAuthenticated]
#     queryset = Comment.objects.all()

#     def perform_create (self, serializer) :
#         serializer.save(author=self.request.user)

# class UpdateDeletePostView (ModelViewSet) :
#     serializer_class = CommentSerializer
#     permission_classes = [IsAuthenticated, IsAuthor]
#     queryset = Post.objects.all()