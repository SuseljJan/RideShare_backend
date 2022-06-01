from rest_framework import serializers

from location.serializers import LocationSerializer
from transport.serializers import TransportSerializer
from transport_requests.models import TransportRequest


class TransportRequestSerializer(serializers.ModelSerializer):
    start_location = LocationSerializer(required=False, allow_null=True)
    end_location = LocationSerializer(required=False, allow_null=True)
    end_location_id = serializers.IntegerField(required=False, allow_null=True, write_only=True)
    start_location_id = serializers.IntegerField(required=False, allow_null=True, write_only=True)
    comment = serializers.CharField(max_length=250, required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = TransportRequest
        exclude = ['passenger']

    def validate(self, attrs):
        transport = attrs['transport']
        campaign = attrs.get('inside_campaign')

        if transport.canceled or transport.passengers_were_found:
            raise serializers.ValidationError({'transport': ['transport offer is closed or canceled']})
        if campaign:
            if campaign and campaign.transport_was_found:
                raise serializers.ValidationError({'campaign': ['campaign is closed']})
            if transport.id in campaign.transport_ids_to_which_requests_were_send():
                raise serializers.ValidationError({'campaign': ['transport request was already sent to the same transport offer under the same campaign']})

        return attrs


class TransportRequestWithTransportInfoSerializer(serializers.ModelSerializer):
    start_location = LocationSerializer(required=False, allow_null=True)
    end_location = LocationSerializer(required=False, allow_null=True)
    end_location_id = serializers.IntegerField(required=False, allow_null=True, write_only=True)
    start_location_id = serializers.IntegerField(required=False, allow_null=True, write_only=True)
    transport = TransportSerializer()

    class Meta:
        model = TransportRequest
        fields = '__all__'