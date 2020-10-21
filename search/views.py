from feed.models import Post
from api.models import User
from feed.serializers import PostSerializer
from api.serializers import userProfileSerializer
from rest_framework.viewsets import ModelViewSet

class UserSearchView (ModelViewSet) :
    serializer_class = userProfileSerializer
    queryset = User.objects.all()

    def get_queryset (self) :
        query = self.request.GET.get('query')
        queryset = self.queryset.filter(username=query)
        return queryset

class PostSearchView (ModelViewSet) :
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get_queryset (self) :
        query = self.request.GET.get('query')
        queryset = self.queryset.filter(title=query)
        return queryset