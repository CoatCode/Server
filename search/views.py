from feed.models import Post
from api.models import User
from feed.serializers import PostSerializer
from api.serializers import userProfileSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

class UserSearchView (ModelViewSet) :
    serializer_class = userProfileSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

    def get_queryset (self) :
        query = self.kwargs['query']
        queryset = self.queryset.filter(username=query)
        return queryset

class PostSearchView (ModelViewSet) :
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()

    def get_queryset (self) :
        query = self.request.GET.get('query', '')
        print(query)
        queryset = self.queryset.filter(title=query)
        return queryset