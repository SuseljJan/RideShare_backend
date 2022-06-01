from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.shortcuts import _get_queryset

from location.models import Location


def get_object_or_400(klass, error_message, *args, **kwargs):
    try:
        return _get_queryset(klass).get(*args, **kwargs)
    except Exception:
        raise serializers.ValidationError({'validation': [error_message]})


def parse_start_and_end_location(serializer):
    if 'start_location_id' in serializer.validated_data and serializer.validated_data['start_location_id'] is not None:
        start_in_db = get_object_or_400(Location, 'start location id is incorrect', id=serializer.validated_data.pop('start_location_id'))
    elif 'start_location' in serializer.validated_data and serializer.validated_data['start_location'] is not None:
        start = serializer.validated_data.pop('start_location')
        start_in_db = Location.objects.create(**start)
    else:
        raise serializers.ValidationError({'start_location': ['start_location or start_location_id must be provided']})

    if 'end_location_id' in serializer.validated_data and serializer.validated_data['end_location_id'] is not None:
        end_in_db = Location.objects.get(id=serializer.validated_data.pop('end_location_id'))
    elif 'end_location' in serializer.validated_data and serializer.validated_data['end_location'] is not None:
        end = serializer.validated_data.pop('end_location')
        end_in_db = Location.objects.create(**end)
    else:
        raise serializers.ValidationError({'end_location': ['end_location or end_location_id must be provided']})

    return {
        'start_location': start_in_db,
        'end_location': end_in_db
    }
