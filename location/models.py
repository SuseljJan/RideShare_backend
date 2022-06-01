from django.contrib.gis.db import models


class Location(models.Model):
    coordinates = models.PointField()
    country = models.CharField(max_length=150, null=True)
    city = models.CharField(max_length=150, null=True)
    street = models.CharField(max_length=150, null=True)
    street_number = models.CharField(max_length=20, null=True)
    postal_code = models.CharField(max_length=150, null=True)
    state = models.CharField(max_length=150, null=True)


class OftenUsedLocation(Location):
    owner = models.ForeignKey('user.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

