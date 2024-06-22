from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext as _

from core.models import BaseModel


class Category(BaseModel):
    """ Category model """
    name = models.CharField(max_length=255, unique=True, verbose_name=_('Name'), help_text=_('Category name'))
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.name


class Post(BaseModel):
    """ Post model """
    title = models.CharField(max_length=255, verbose_name=_('Title'), help_text=_('Post title'))
    content = models.TextField(verbose_name=_('Content'), help_text=_('Post content'))
    published = models.BooleanField(default=False, verbose_name=_('Published'), help_text=_('Post published status'))
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts', verbose_name=_('Author'), help_text=_('Post author'),
    )
    categories = models.ManyToManyField(
        Category, related_name='posts', verbose_name=_('Categories'), help_text=_('Post categories'),
    )

    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')

    def __str__(self):
        return self.title


class Comment(BaseModel):
    """ Comment model """
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments', verbose_name=_('Post'), help_text=_('Post comment'),
    )
    content = models.TextField(verbose_name=_('Content'), help_text=_('Comment content'))
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments', verbose_name=_('Author'),
        help_text=_('Comment author'),
    )

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'
