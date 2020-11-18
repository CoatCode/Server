from feed.models import Post
from api.models import User
from feed.serializers import PostSerializer
from api.serializers import userProfileSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination

class LargeResultsSetPagination (PageNumberPagination) :
    page_size = 15
    page_query_param = 'page'
    max_page_size = 100

    def get_paginated_response (self, data) :
        return Response(data)

class UserSearchView (ModelViewSet) :
    serializer_class = userProfileSerializer
    queryset = User.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['username']
    pagination_class = LargeResultsSetPagination

class PostSearchView (ModelViewSet) :
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['title']
    pagination_class = LargeResultsSetPagination