from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.CharField(unique=True, max_length=255)
    password = models.CharField(max_length=255)
    username = None

    # making username none and USERNAME_FIELD to 'email' to make login system use email as USERNAME field

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []
