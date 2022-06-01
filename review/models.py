import django
from django.db import models


class Review(models.Model):
    number_of_stars = models.IntegerField()
    comment = models.CharField(max_length=250)
    created_at = models.DateTimeField(default=django.utils.timezone.now)
    reviewed = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='reviewed')
    reviewer = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='reviewer')
