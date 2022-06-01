from datetime import datetime
import django
from django.db import models

class Message(models.Model):
    receiver = models.ForeignKey('user.User', on_delete=models.CASCADE)
    posted = models.DateTimeField(default=django.utils.timezone.now)
    message = models.CharField(max_length=150)
    archived = models.BooleanField(default=False)
    read = models.BooleanField(default=False)
