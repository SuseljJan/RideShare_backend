from django.contrib.gis.db import models
import django
from django.db.models import Sum, Case, When, F

from transport_requests.models import TransportRequest


class Negotiability(models.Model):
    date_is_negotiable = models.BooleanField(default=False)
    time_is_negotiable = models.BooleanField(default=True)
    price_is_negotiable = models.BooleanField(default=True)
    number_of_seats_are_negotiable = models.BooleanField(default=True)
    start_location_is_negotiable = models.BooleanField(default=True)
    end_location_is_negotiable = models.BooleanField(default=True)

class Transport(models.Model):
    date = models.DateField()
    time = models.TimeField()
    price = models.FloatField()
    number_of_seats = models.IntegerField()
    driver = models.ForeignKey('user.User', related_name='driver', on_delete=models.PROTECT)
    start_location = models.ForeignKey('location.Location', related_name='start_location', on_delete=models.PROTECT)
    end_location = models.ForeignKey('location.Location', related_name='end_location', on_delete=models.PROTECT)
    passengers_were_found = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=django.utils.timezone.now)
    comment = models.CharField(max_length=250, null=True)
    negotiability = models.ForeignKey(Negotiability, related_name='negotiability', on_delete=models.CASCADE)
    canceled = models.BooleanField(default=False)

    def number_of_accepted_offers(self):
        return TransportRequest.objects.filter(transport=self.id, accepted_by_driver=True).count()


    def get_still_available_seats(self):
        all_seats = self.number_of_seats
        taken_seats = self.passengers.aggregate(seats=Sum(Case(When(accepted_by_driver=True, then=F('number_of_seats')))))['seats'] or 0

        return all_seats - taken_seats

