from .models import post, comment
from .serializers import postSerializer, commentSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

class postView (ModelViewSet) :
    serializer_class = postSerializer
    permission_classes = [IsAuthenticated]
    queryset = post.objects.all()

    def perform_create (self, serializer) :
        serializer.save(author=self.request.user)

class commentView (ModelViewSet) :
    serializer_class = commentSerializer
    permission_classes = [IsAuthenticated]
    queryset = comment.objects.all()

    def perform_create (self, serializer) :
        serializer.save(author=self.request.user)