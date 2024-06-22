from typing import Optional, Union

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase

from blog.models import Category, Post, Comment


def get_user_data(num: int) -> dict:
    """ Get user data """
    return {
        'username': f'test{num}',
        'password': f'test{num}',
    }


def get_post_data(num: int, author: Optional[Union[User, int]] = None) -> dict:
    """ Get post data """
    data = {
        'title': f'Test {num}',
        'content': f'Test post {num}',
        'published': True,
    }
    if author:
        data['author'] = author
    return data


def get_category_data(num: int) -> dict:
    """ Get category data """
    return {
        'name': f'Test {num}',
        'description': f'Test category {num}',
    }


def comment_data(num: int, user: Union[User, int], post: Union[Post, int]) -> dict:
    """ Get comment data """
    return {
        'content': f'Test comment {num}',
        'author': user,
        'post': post,
    }


class PostTestCase(TestCase):
    """ Post model test case """

    def setUp(self):
        """ Set up test data """
        # Create dependencies (user and category)
        self.user = User.objects.create_user(**get_user_data(1))
        self.category = Category.objects.create(**get_category_data(1))
        # Create post
        self.post = Post.objects.create(**get_post_data(num=1, author=self.user))
        # Add category to post
        self.post.categories.add(self.category)

    def test_create_post(self):
        """ Test create post """
        # Check post data
        data = get_post_data(num=1, author=self.user)
        self.assertEqual(self.post.title, data.get('title'))
        self.assertEqual(self.post.content, data.get('content'))
        self.assertEqual(self.post.published, data.get('published'))
        self.assertEqual(self.post.author, self.user)
        self.assertEqual(self.post.categories.count(), 1)

        # Check post count
        Post.objects.create(**get_post_data(num=2, author=self.user))
        self.assertEqual(Post.objects.count(), 2)

    def test_update_post(self):
        """ Test update post """
        # Create dependencies (user and category)
        user = User.objects.create_user(**get_user_data(2))
        category = Category.objects.create(**get_category_data(2))
        # Update post data
        data = get_post_data(num=2, author=user)
        self.post.title = data.get('title')
        self.post.content = data.get('content')
        self.post.published = data.get('published')
        self.post.author = user
        self.post.categories.clear()
        self.post.categories.add(category)
        self.post.save()

        # Check post data
        self.assertEqual(self.post.content, data.get('content'))
        self.assertEqual(self.post.title, data.get('title'))
        self.assertEqual(self.post.published, data.get('published'))
        self.assertEqual(self.post.author, user)
        self.assertEqual(self.post.categories.first(), category)

    def test_delete_post(self):
        """ Test delete post """
        # Check post count
        self.assertEqual(Post.objects.count(), 1)
        self.post.delete()
        self.assertEqual(Post.objects.count(), 0)


class CategoryTestCase(TestCase):
    """ Category model test case """

    def setUp(self):
        """ Set up test data """
        # Create category
        self.category = Category.objects.create(**get_category_data(1))

    def test_create_category(self):
        """ Test create category """
        # Check category data
        data = get_category_data(1)
        self.assertEqual(self.category.name, data.get('name'))
        self.assertEqual(self.category.description, data.get('description'))

        # Check category count
        Category.objects.create(**get_category_data(2))
        self.assertEqual(Category.objects.count(), 2)
        # Check unique constraint
        with self.assertRaises(Exception):
            Category.objects.create(**get_category_data(1))

    def test_update_category(self):
        """ Test update category """
        # Update category data
        data = get_category_data(2)
        self.category.name = data.get('name')
        self.category.description = data.get('description')
        self.category.save()

        # Check category data
        self.assertEqual(self.category.name, data.get('name'))
        self.assertEqual(self.category.description, data.get('description'))
        self.assertEqual(Category.objects.count(), 1)

    def test_delete_category(self):
        """ Test delete category """
        # Check category count
        self.assertEqual(Category.objects.count(), 1)
        self.category.delete()
        self.assertEqual(Category.objects.count(), 0)


class CommentTestCase(TestCase):
    """ Comment model test case """

    def setUp(self):
        """ Set up test data """
        # Create dependencies (user, category, and post)
        self.user = User.objects.create_user(**get_user_data(1))
        self.post = Post.objects.create(**get_post_data(num=1, author=self.user))
        # Create comment
        self.comment = Comment.objects.create(**comment_data(1, self.user, self.post))

    def test_create_comment(self):
        """ Test create comment """
        # Check comment data
        data = comment_data(1, self.user, self.post)
        self.assertEqual(self.comment.content, data.get('content'))
        self.assertEqual(self.comment.author, self.user)
        self.assertEqual(self.comment.post, self.post)

        # Check comment count
        Comment.objects.create(**comment_data(2, self.user, self.post))
        self.assertEqual(Comment.objects.count(), 2)

    def test_update_comment(self):
        """ Test update comment """
        # Create dependencies (user, category, and post)
        self.user = User.objects.create_user(**get_user_data(2))
        self.post = Post.objects.create(**get_post_data(num=2, author=self.user))
        # Update comment data
        data = comment_data(2, self.user, self.post)
        self.comment.content = data.get('content')
        self.comment.author = self.user
        self.comment.post = self.post
        self.comment.save()

        # Check comment data
        self.assertEqual(self.comment.content, data.get('content'))
        self.assertEqual(self.comment.author, self.user)
        self.assertEqual(self.comment.post, self.post)
        self.assertEqual(Comment.objects.count(), 1)

    def test_delete_comment(self):
        """ Test delete comment """
        # Check comment count
        self.assertEqual(Comment.objects.count(), 1)
        self.comment.delete()
        self.assertEqual(Comment.objects.count(), 0)


class PostAPITestCase(APITestCase):
    """ Post API test case """

    def setUp(self):
        """ Set up test data """
        # Create user
        self.user = User.objects.create_user(**get_user_data(1))
        self.client.force_authenticate(user=self.user)
        # Create post
        self.post = Post.objects.create(**get_post_data(num=1, author=self.user))

    def test_create_post(self):
        """ Test create post """
        data = get_post_data(num=2, author=self.user.id)
        response = self.client.post(reverse('blog:post-list'), data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Post.objects.count(), 2)

    def test_update_post(self):
        """ Test update post """
        data = get_post_data(num=2, author=self.user)
        response = self.client.put(reverse('blog:post-detail', args=[self.post.id]), data)
        self.assertEqual(response.status_code, 200)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, data.get('title'))
        self.assertEqual(self.post.content, data.get('content'))
        self.assertEqual(self.post.published, data.get('published'))

    def test_delete_post(self):
        """ Test delete post """
        response = self.client.delete(reverse('blog:post-detail', args=[self.post.id]))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Post.objects.count(), 0)


class CategoryAPITestCase(APITestCase):
    """ Category API test case """

    def setUp(self):
        """ Set up test data """
        # Create user
        self.user = User.objects.create_user(**get_user_data(1))
        self.client.force_authenticate(user=self.user)
        # Create category
        self.category = Category.objects.create(**get_category_data(1))

    def test_create_category(self):
        """ Test create category """
        data = get_category_data(2)
        response = self.client.post(reverse('blog:category-list'), data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Category.objects.count(), 2)

    def test_update_category(self):
        """ Test update category """
        data = get_category_data(2)
        response = self.client.put(reverse('blog:category-detail', args=[self.category.id]), data)
        self.assertEqual(response.status_code, 200)
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, data.get('name'))
        self.assertEqual(self.category.description, data.get('description'))

    def test_delete_category(self):
        """ Test delete category """
        response = self.client.delete(reverse('blog:category-detail', args=[self.category.id]))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Category.objects.count(), 0)


class CommentAPITestCase(APITestCase):
    """ Comment API test case """

    def setUp(self):
        """ Set up test data """
        # Create user
        self.user = User.objects.create_user(**get_user_data(1))
        self.client.force_authenticate(user=self.user)
        # Create post
        self.post = Post.objects.create(**get_post_data(num=1, author=self.user))
        # Create comment
        self.comment = Comment.objects.create(**comment_data(1, self.user, self.post))

    def test_create_comment(self):
        """ Test create comment """
        data = comment_data(2, self.user.id, self.post.id)
        response = self.client.post(reverse('blog:comment-list'), data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Comment.objects.count(), 2)

    def test_update_comment(self):
        """ Test update comment """
        data = comment_data(2, self.user.id, self.post.id)
        response = self.client.put(reverse('blog:comment-detail', args=[self.comment.id]), data)
        self.assertEqual(response.status_code, 200)
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.content, data.get('content'))

    def test_delete_comment(self):
        """ Test delete comment """
        response = self.client.delete(reverse('blog:comment-detail', args=[self.comment.id]))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Comment.objects.count(), 0)
