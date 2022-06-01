from django.contrib.auth.models import AbstractUser
from django.db import models

from review.models import Review
from transport.models import Transport


class User(AbstractUser):
    #email = models.CharField(max_length=150)
    is_banned = models.BooleanField(default=False)
    notify_by_SMS = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=30, null=True)
    paypal_mail = models.CharField(max_length=150, null=True)
