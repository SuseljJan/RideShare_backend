from rest_framework import mixins, serializers
from django.contrib.gis.db.models.functions import Distance
from django.db.models import QuerySet, Func, ExpressionWrapper, FloatField, Model
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import BaseSerializer

from location.models import OftenUsedLocation
from location.serializers import OftenUsedLocationSerializer
from django.contrib.gis.geos import GEOSGeometry


class OftenUsedLocationsNotPaginatedViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    pagination_class = None
    permission_classes = [IsAuthenticated]
    serializer_class = OftenUsedLocationSerializer

    def get_queryset(self) -> QuerySet:
        user_id = self.request.user.id

        return OftenUsedLocation.objects\
            .filter(owner=user_id)\
            .annotate(
                lat=ExpressionWrapper(Func('coordinates', function='ST_Y'), output_field=FloatField()),
                lan=ExpressionWrapper(Func('coordinates', function='ST_X'), output_field=FloatField()),
            )


class OftenUsedLocationViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = OftenUsedLocationSerializer

    def get_queryset(self) -> QuerySet:
        user_id = self.request.user.id
        # TODO: make it work for actual location
        search_location = GEOSGeometry('POINT(1 1)', srid=4326)

        return OftenUsedLocation.objects.filter(owner=user_id).annotate(
            lat=ExpressionWrapper(Func('coordinates', function='ST_Y'), output_field=FloatField()),
            lan=ExpressionWrapper(Func('coordinates', function='ST_X'), output_field=FloatField()),
            distance=Distance('coordinates', search_location),
        ).order_by('distance')

    def perform_create(self, serializer: BaseSerializer) -> None:
        # breakpoint()
        user_id = self.request.user.id

        # must be unique per user
        if OftenUsedLocation.objects.filter(name=serializer.validated_data['name'], owner=user_id).exists():
            raise serializers.ValidationError({'name': ['name must be unique']})

        user = self.request.user
        serializer.save(owner=user)

    def perform_destroy(self, instance: Model) -> None:
        if instance.owner.id == self.request.user.id:
            instance.delete(keep_parents=True)
        else:
            raise PermissionDenied()

