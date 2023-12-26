from django.contrib.auth.models import AbstractUser
from django.db import models

from api import constants


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE_CHOICES = (
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
    )
    username = models.CharField(
        verbose_name='Логин пользователя',
        help_text='Укажите логин',
        max_length=constants.MAX_USERNAME_FIRST_NAME_LAST_NAME_LENGTH,
        unique=True,
        blank=False,
        null=False,
    )
    first_name = models.CharField(
        verbose_name='Имя пользователя',
        help_text='Укажите Ваше имя',
        max_length=constants.MAX_USERNAME_FIRST_NAME_LAST_NAME_LENGTH,
        blank=True,
    )
    last_name = models.CharField(
        verbose_name='Фамилия пользователя',
        help_text='Укажите Вашу фамилию',
        max_length=constants.MAX_USERNAME_FIRST_NAME_LAST_NAME_LENGTH,
        blank=True,
    )
    role = models.CharField(
        verbose_name='Роль пользователя',
        max_length=constants.MAX_SLUG_ROLE_LENGTH,
        choices=ROLE_CHOICES,
        blank=True,
        default=USER,
    )
    email = models.EmailField(
        verbose_name='Адрес электронной почты пользователя',
        help_text='Укажите адрес электронной почты',
        max_length=constants.MAX_EMAIL_LENGTH,
        unique=True,
        blank=False,
        null=False,
    )
    bio = models.TextField(
        verbose_name='Биография пользователя',
        help_text='Расскажите о себе',
        blank=True
    )

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = ('id',)
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_user',
            )
        ]

    def __str__(self):
        return self.username
