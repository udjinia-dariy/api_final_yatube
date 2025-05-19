from django.urls import path, include
from rest_framework.routers import SimpleRouter

from api.views import PostViewSet, GroupViewSet, CommentViewSet, FollowViewSet

router = SimpleRouter()
router.register(r'follow', FollowViewSet, basename='follow')
router.register(r'groups', GroupViewSet)
router.register(r'posts', PostViewSet)
router.register(
    r'posts/(?P<post_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
]
