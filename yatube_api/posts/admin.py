from django.contrib import admin

from .models import Group, Post, Comment, Follow

admin.site.empty_value_display = '-'


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'title',
        'slug',
        'description',
    )
    prepopulated_fields = {'slug': ('title',), }
    search_fields = ('title', 'slug',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'text',
        'author',
        'group',
        'image',
        'pub_date',
    )
    list_filter = ('pub_date', 'author', 'group',)
    search_fields = ('text',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'text',
        'author',
        'post',
        'created',
    )
    list_filter = ('created', 'author', 'post',)
    search_fields = ('text',)


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'following',
    )
    list_filter = ('user', 'following',)
    list_display_links = ('user', 'following')
