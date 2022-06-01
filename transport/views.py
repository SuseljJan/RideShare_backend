from datetime import date

import django_filters
from django.contrib.gis.measure import D
from rest_framework import filters, mixins, serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer

from campaign.models import Campaign
from common.helper_functions import get_object_or_400, parse_start_and_end_location
from location.models import Location
from review.models import Review
from transport.models import Transport, Negotiability
from transport.serializers import TransportSerializer, GivenTransportSerializer, TransportWithNegotiabilitySerializer
from django.db.models import F, QuerySet, Avg, Count, Q, Case, When, Value, CharField, BooleanField
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.db.models.functions import Distance

from transport_requests.models import TransportRequest


class TransportWithNegotiabilityViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = Transport.objects.all()
    serializer_class = TransportWithNegotiabilitySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self) -> QuerySet:
        if self.request.resolver_match.url_name != 'transport-list':
            return super()\
                .get_queryset()\
                .annotate(driver_avg_rating=Avg(F('driver__reviewed__number_of_stars'))) \
                .annotate(driver_number_of_ratings=Count(F('driver__reviewed')))
        else:
            raise serializers.ValidationError({'err': 'querying for lists not allowed on this endpoint'})


class TransportViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin):
    queryset = Transport.objects.all()
    serializer_class = TransportSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]
    ordering_fields = '__all__'
    search_fields = ['driver__email']
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer: BaseSerializer) -> None:
        user = self.request.user
        start_and_end = parse_start_and_end_location(serializer)
        negotiability = Negotiability.objects.create(**serializer.validated_data.pop('negotiability'))

        serializer.save(start_location=start_and_end['start_location'], end_location=start_and_end['end_location'], driver=user, negotiability=negotiability)

    def get_object(self):
        transport_obj = Transport.objects.get(id=int(self.kwargs['pk']))
        reviews = Review.objects.filter(reviewed=transport_obj.driver)
        transport_obj.driver_avg_rating = reviews.aggregate(Avg('number_of_stars'))['number_of_stars__avg']
        transport_obj.driver_number_of_ratings = reviews.count()

        return transport_obj

    def get_queryset(self):
        try:
            start_lan = float(self.request.query_params.get('start_lan', None))
            start_lat = float(self.request.query_params.get('start_lat', None))
            end_lan = float(self.request.query_params.get('end_lan', None))
            end_lat = float(self.request.query_params.get('end_lat', None))
            time_from = self.request.query_params.get('time_from', None)
            time_to = self.request.query_params.get('time_to', None)
            date = self.request.query_params.get('date', None)
            start = GEOSGeometry('POINT({} {})'.format(start_lan, start_lat), srid=4326)
            end = GEOSGeometry('POINT({} {})'.format(end_lan, end_lat), srid=4326)

            if not (start_lan and start_lat and end_lan and end_lat and time_from and time_to and date):
                raise Exception
        except Exception:
            raise serializers.ValidationError({'query parameters': ['required query params are start_lat, start_lan'
                                                                    'start_lat, start_lan, time_from, time_to and date']})

        # TODO remove all results for past days or set as invalid search query if it's in the past
        # TODO must be careful about using current time (might be different than client's current time)
        return super() \
            .get_queryset() \
            .filter(passengers_were_found=False) \
            .filter(date=date) \
            .filter(time__gte=time_from) \
            .filter(time__lte=time_to) \
            .filter(canceled=False) \
            .annotate(driver_avg_rating=Avg(F('driver__reviewed__number_of_stars'))) \
            .annotate(driver_number_of_ratings=Count(F('driver__reviewed'))) \
            .annotate(distance_from_start_location_in_km=Distance('start_location__coordinates', start))\
            .annotate(distance_from_end_location_in_km=Distance('end_location__coordinates', end))\
            .annotate(distance_off_requested_location=F('distance_from_end_location_in_km')+F('distance_from_start_location_in_km'))\
            .order_by(F('distance_off_requested_location'))\
            .filter(distance_off_requested_location__lte=D(km=200))


class GivenTransportsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = GivenTransportSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet:
        # When passengers were not found and date of transport is greater or equal than today it is active otherwise no
        return Transport.objects\
            .filter(driver=self.request.user.id)\
            .annotate(active=Case(When(passengers_were_found=True, then=Value('false')),
                                  When(canceled=True, then=Value('false')),
                                  When(date__gte=date.today(), then=Value('true')),
                                  default=Value('false'), output_field=BooleanField()))\
            .order_by('canceled', '-active', '-created_at')



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def cancel_transport(request, id):
    user = request.user
    transport = get_object_or_400(Transport, 'transport', id=id)

    if not transport.driver.id == user.id:
        return Response(status=status.HTTP_403_FORBIDDEN)

    if transport.number_of_accepted_offers() > 0:
        return Response({'transport': ['transport cannot be canceled when it already has accepted transport request/s associated with it']}, status=status.HTTP_400_BAD_REQUEST)

    transport.canceled = True
    transport.save()
    return Response(status=status.HTTP_204_NO_CONTENT)




