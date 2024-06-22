from rest_framework import routers

from blog.views import PostModelViewSet, CategoryModelViewSet, CommentModelViewSet


app_name = 'blog'

router = routers.DefaultRouter()
router.register(prefix=r'posts', viewset=PostModelViewSet, basename='post')
router.register(prefix=r'categories', viewset=CategoryModelViewSet, basename='category')
router.register(prefix=r'comments', viewset=CommentModelViewSet, basename='comment')

urlpatterns = router.urls
