from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator


PUBLIC_VERBOSE_LENGTH = 15


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLES = ((ADMIN, 'admin'),
             (MODERATOR, 'moderator'),
             (USER, 'user'),)

    username = models.CharField(max_length=150, blank=False, unique=True,
                                validators=(UnicodeUsernameValidator(),))
    email = models.EmailField(blank=False, unique=True)
    role = models.CharField(choices=ROLES, default=USER, max_length=20)
    bio = models.TextField(blank=True, null=True)

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN


class Category(models.Model):
    name = models.CharField(
        max_length=256, unique=True,
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=50, unique=True,
        verbose_name='Идентификатор'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name[:PUBLIC_VERBOSE_LENGTH]


class Genre(models.Model):
    name = models.CharField(
        max_length=256, unique=True,
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=50, unique=True,
        verbose_name='Идентификатор'
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name[:PUBLIC_VERBOSE_LENGTH]


class Title(models.Model):
    category = models.ForeignKey(
        Category,
        null=True, on_delete=models.SET_NULL,
        related_name='titles', verbose_name='Категория'
    )
    genre = models.ManyToManyField(Genre, through='GenreTitle')
    name = models.CharField(max_length=256, verbose_name='Название')
    description = models.TextField(
        blank=True, null=True, verbose_name='Описание'
    )
    year = models.IntegerField()

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:PUBLIC_VERBOSE_LENGTH]


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Связь произведения и его жанра'
        verbose_name_plural = 'Связи произведений и их жанров'

    def __str__(self):
        return f'{self.title}: {self.genre}'

