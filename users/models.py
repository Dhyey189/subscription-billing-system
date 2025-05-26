from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class TimeStampedModel(models.Model):
    """
    An abstract model, that can be used as base model to track record's created and updated
    time.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser, TimeStampedModel):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
