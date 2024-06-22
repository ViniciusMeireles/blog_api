from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from blog.models import Post, Category, Comment
from blog.serializers import PostSerializer, CategorySerializer, CommentSerializer


class PostModelViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ['get', 'post', 'put', 'delete']

    def perform_create(self, serializer):
        """ Add author to post """
        serializer.save(author=self.request.user)


class CategoryModelViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ['get', 'post', 'put', 'delete']


class CommentModelViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ['get', 'post', 'put', 'delete']
