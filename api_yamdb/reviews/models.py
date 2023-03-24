from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator


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
