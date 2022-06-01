from django.apps import AppConfig
from django.db.models.signals import post_save


class CampaignConfig(AppConfig):
    name = 'campaign'

    def ready(self):
        from campaign.signals import on_campaign_closed
        post_save.connect(on_campaign_closed, sender='campaign.Campaign')
