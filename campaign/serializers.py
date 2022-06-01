from rest_framework import serializers
from campaign.models import Campaign
from user.serializers import UserSerializerForCampaigns


class CampaignSerializer(serializers.ModelSerializer):
    owner = UserSerializerForCampaigns(read_only=True)

    class Meta:
        model = Campaign
        fields = '__all__'

    def validate(self, attrs):
        # Name must be unique among user's campaigns
        user = self.context['request'].user
        if Campaign.objects.filter(owner=user.id, name=attrs['name']).count() > 0:
            raise serializers.ValidationError({'name': ['campaign name must be unique']})
        return attrs
