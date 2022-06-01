from rest_framework import serializers
from location.serializers import LocationSerializer
from transport.models import Transport, Negotiability
from user.serializers import UserSerializer, UserSerializerForTransportList, GenericUserSerializer


class GivenTransportSerializer(serializers.ModelSerializer):
    driver = GenericUserSerializer()
    start_location = LocationSerializer()
    end_location = LocationSerializer()
    active = serializers.BooleanField()

    class Meta:
        model = Transport
        exclude = ['negotiability']


class NegotiabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Negotiability
        fields = '__all__'


class TransportWithNegotiabilitySerializer(serializers.ModelSerializer):
    driver = UserSerializerForTransportList(read_only=True)
    driver_avg_rating = serializers.FloatField(read_only=True)
    driver_number_of_ratings = serializers.FloatField(read_only=True)
    start_location = LocationSerializer(required=False, allow_null=True)
    end_location = LocationSerializer(required=False, allow_null=True)
    negotiability = NegotiabilitySerializer()

    still_available_seats = serializers.SerializerMethodField()

    class Meta:
        model = Transport
        fields = '__all__'

    def get_still_available_seats(self, obj):
        return obj.get_still_available_seats()


class TransportSerializer(serializers.ModelSerializer):
    driver = UserSerializerForTransportList(read_only=True)
    driver_avg_rating = serializers.FloatField(read_only=True)
    driver_number_of_ratings = serializers.FloatField(read_only=True)
    start_location = LocationSerializer(required=False, allow_null=True)
    end_location = LocationSerializer(required=False, allow_null=True)
    end_location_id = serializers.IntegerField(required=False, allow_null=True, write_only=True)
    start_location_id = serializers.IntegerField(required=False, allow_null=True, write_only=True)

    distance_from_start_location_in_km = serializers.FloatField(source='distance_from_start_location_in_km.km', read_only=True)
    distance_from_end_location_in_km = serializers.FloatField(source='distance_from_end_location_in_km.km', read_only=True)
    distance_off_requested_location = serializers.FloatField(source='distance_off_requested_location.km', read_only=True)
    still_available_seats = serializers.SerializerMethodField()
    comment = serializers.CharField(max_length=250, required=False, allow_null=True, allow_blank=True)
    negotiability = NegotiabilitySerializer()

    class Meta:
        model = Transport
        fields = '__all__'

    def get_still_available_seats(self, obj):
        return obj.get_still_available_seats()


class TakenTransportSerializer(serializers.ModelSerializer):
    start_location = LocationSerializer()
    end_location = LocationSerializer()
    driver = UserSerializer()

    class Meta:
        model = Transport
        fields = '__all__'

