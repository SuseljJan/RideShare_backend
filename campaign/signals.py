from django.db.models.signals import post_save
from django.dispatch import receiver

from campaign.models import Campaign
from transport_requests.models import TransportRequest


@receiver(post_save, sender=Campaign)
def on_campaign_closed(sender, instance, created, **kwargs):
    if instance.transport_was_found:
        requests = TransportRequest.objects.filter(inside_campaign=instance.id)
        for request in requests:
            request.transport_found = False
            request.save()
