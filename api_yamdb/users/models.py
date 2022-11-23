from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'

    ROLE_CHOISES = (
        (ADMIN, 'Администратор'),
        (USER, 'Простой смертный'),
        (MODERATOR, 'Модератор'),
    )

    first_name = models.CharField(
        'first name',
        max_length=150,
        blank=True
    )
    email = models.EmailField(
        'email address',
        blank=True,
        unique=True
    )
    bio = models.TextField(
        blank=True,
        verbose_name='Биография',
    )

    role = models.CharField(
        'Роль',
        max_length=20,
        choices=ROLE_CHOISES,
        default=USER,
        blank=False,
        null=False,
    )

    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=30,
        unique=True,
        blank=True,
        null=True)

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_moderator(self):
        return self.role == User.MODERATOR

    @property
    def is_admin(self):
        return self.role == User.ADMIN

    @property
    def is_user(self):
        return self.role == User.USER
