from django.shortcuts import get_object_or_404

from rest_framework.viewsets import (
    ModelViewSet,
    ReadOnlyModelViewSet,
    GenericViewSet
)
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated
)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import mixins
from rest_framework import filters

from api.serializers import (
    CommentSerializer, PostSerializer,
    GroupSerializer, FollowSerializer
)
from posts.models import Post, Comment, Group, Follow
from .permissions import IsAuthorOrReadOnly


class GroupViewSet(ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)

    def get_queryset(self):
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        return post.comments.all()


class FollowViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)
