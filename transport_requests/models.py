from django.db import models
import django

from location.models import Location



class TransportRequest(models.Model):
    date = models.DateField()
    time = models.TimeField()
    price = models.FloatField()
    number_of_seats = models.IntegerField()
    inside_campaign = models.ForeignKey('campaign.Campaign', related_name='campaign', on_delete=models.PROTECT, null=True, blank=True)
    start_location = models.ForeignKey(Location, related_name='offer_start_location', on_delete=models.PROTECT)
    end_location = models.ForeignKey(Location, related_name='offer_end_location', on_delete=models.PROTECT)
    created_at = models.DateTimeField(default=django.utils.timezone.now)
    comment = models.CharField(max_length=250, null=True)
    transport = models.ForeignKey('transport.Transport', related_name='passengers', on_delete=models.PROTECT)
    passenger = models.ForeignKey('user.User', related_name='as_passenger', on_delete=models.PROTECT)
    accepted_by_driver = models.BooleanField(default=False)
    transport_found = models.BooleanField(default=False)
