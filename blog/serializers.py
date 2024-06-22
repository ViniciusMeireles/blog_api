from django.contrib.auth.models import User
from rest_framework import serializers

from blog.models import Category, Comment, Post


class UserSerializer(serializers.ModelSerializer):
    """ User model serializer """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class CategorySerializer(serializers.ModelSerializer):
    """ Category model serializer """
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


class CommentSerializer(serializers.ModelSerializer):
    """ Comment model serializer """
    class Meta:
        model = Comment
        fields = ['id', 'post', 'content', 'author', 'created_at', 'updated_at']


class PostSerializer(serializers.ModelSerializer):
    """ Post model serializer """
    author = UserSerializer(read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'content', 'published', 'author', 'categories', 'comments', 'created_at', 'updated_at'
        ]
