from django.db import models
from django.contrib.auth.models import AbstractUser

USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'

ROLE_CHOICES = [
    (USER, USER),
    (ADMIN, ADMIN),
    (MODERATOR, MODERATOR),
]


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        blank=False,
        null=False
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        blank=False,
        null=False
    )
    role = models.CharField(
        'роль',
        max_length=20,
        choices=ROLE_CHOICES,
        default=USER,
        blank=True
    )
    bio = models.TextField(
        'биография',
        blank=True,
    )
    first_name = models.CharField(
        'имя',
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        'фамилия',
        max_length=150,
        blank=True
    )

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(
        'id',
        max_length=200,
    )
    slug = models.SlugField(
        unique=True,
        db_index=True
    )

    def __str__(self):
        return f'{self.name} {self.name}'


class Title(models.Model):
    name = models.CharField(
        'название',
        max_length=200,
        db_index=True
    )
    year = models.IntegerField(
        'год',
    )
    category = models.CharField(
        'категория',
        max_length=150,
        blank=True
    )
    genre = models.CharField(
        'жанр',
        max_length=150,
        blank=True
    )

    def __str__(self):
        return self.name
