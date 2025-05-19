from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    """Group model for DB
    Columns:
        title - Char[128];
        slug - Slug, unique;
        description - Text.
    """

    title = models.CharField(max_length=128, verbose_name='Заголовок')
    slug = models.SlugField(unique=True, verbose_name='Slug')
    description = models.TextField(verbose_name='Описание')

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return self.title


class Post(models.Model):
    """Post model for DB
    Columns:
        text - Text;
        pub_date - DateTime, auto_now_add;
        author - ForeignKey(User), delete cascade, related_name posts;
        image - Image, upload_to posts/, null=True, blank=True;
        group - ForeignKey(Group), delete set_null, null=True,
            blank=True, related_name posts;
    """

    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор'
    )
    image = models.ImageField(
        upload_to='posts/',
        null=True,
        blank=True,
        verbose_name='Изображение'
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        related_name='posts',
        blank=True,
        null=True,
        verbose_name='Группа'
    )

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-pub_date']


class Comment(models.Model):
    """Comment model for DB
    Columns:
        author - ForeignKey(User), delete cascade, related_name comments;
        post - ForeignKey(Post), delete cascade, related_name comments;
        text - Text;
        created - DateTime, auto_now_add
    """
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Пост'
    )
    text = models.TextField(verbose_name='Текст')
    created = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата добавления'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-created',)

    def str(self):
        return self.text


class Follow(models.Model):
    """Follow model for DB
    Columns:
        user - ForeignKey(User), delete cascade, related_name follower;
        following - ForeignKey(User), delete cascade, related_name following
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Подписан'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='unique_follow'
            )
        ]
