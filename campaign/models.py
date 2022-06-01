import django
from django.db import models

from transport_requests.models import TransportRequest


class Campaign(models.Model):
    name = models.CharField(max_length=150)
    transport_was_found = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=django.utils.timezone.now)
    owner = models.ForeignKey('user.User', on_delete=models.CASCADE)

    def transport_ids_to_which_requests_were_send(self):
        transports = TransportRequest.objects.filter(inside_campaign=self.id).values('transport__id')
        return [transport['transport__id'] for transport in transports]
