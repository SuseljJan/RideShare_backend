from rest_framework import serializers
from location.business_logic.coordinates_conversion import latlng_to_coordinates, coordinates_to_latlng
from location.models import OftenUsedLocation, Location


class LocationSerializer(serializers.ModelSerializer):
    street_number = serializers.CharField(max_length=20, required=False, allow_blank=True, allow_null=True)
    street = serializers.CharField(max_length=150, required=False, allow_blank=True, allow_null=True)
    city = serializers.CharField(max_length=150, required=False, allow_blank=True, allow_null=True)
    country = serializers.CharField(max_length=150, required=False, allow_blank=True, allow_null=True)
    lat = serializers.FloatField(allow_null=True)
    lan = serializers.FloatField(allow_null=True)

    class Meta:
        model = Location
        exclude = ['coordinates']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        latlng = coordinates_to_latlng(instance.coordinates)
        ret['lan'] = latlng[0]
        ret['lat'] = latlng[1]
        return ret

    def to_internal_value(self, data):
        data['coordinates'] = latlng_to_coordinates(data.pop('lat'), data.pop('lan'))
        return data


class OftenUsedLocationSerializer(serializers.ModelSerializer):
    street_number = serializers.CharField(max_length=20, required=False, allow_blank=True, allow_null=True)
    street = serializers.CharField(max_length=150, required=False, allow_blank=True, allow_null=True)
    city = serializers.CharField(max_length=150, required=False, allow_blank=True, allow_null=True)
    country = serializers.CharField(max_length=150, required=False, allow_blank=True, allow_null=True)
    lat = serializers.FloatField(allow_null=True)
    lan = serializers.FloatField(allow_null=True)
    distance = serializers.FloatField(source='distance.km', read_only=True)

    class Meta:
        model = OftenUsedLocation
        exclude = ['coordinates', 'owner']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        latlng = coordinates_to_latlng(instance.coordinates)
        ret['lan'] = latlng[0]
        ret['lat'] = latlng[1]
        return ret

    def to_internal_value(self, data):
        data['coordinates'] = latlng_to_coordinates(data.pop('lat'), data.pop('lan'))
        return data
