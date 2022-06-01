from django.db.models import QuerySet
from rest_framework import viewsets, mixins, status, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from alert_messages.notifications.send_notifications import notify_passenger_about_his_accepted_offer
from campaign.models import Campaign
from common.helper_functions import parse_start_and_end_location
from common.messaging import send_transport_request_received_message, transport_request_accepted_message, transport_found_all_passengers_message
from location.models import Location
from transport.models import Transport
from transport_requests.models import TransportRequest
from transport_requests.serializers import TransportRequestSerializer, TransportRequestWithTransportInfoSerializer
from rest_framework.serializers import BaseSerializer


class TransportRequestViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin):
    serializer_class = TransportRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet:
        transport_id = self.request.query_params.get('transport_id', None)
        accepted = self.request.query_params.get('accepted', None)

        if not Transport.objects.get(id=transport_id).driver.id == self.request.user.id:
            raise PermissionDenied()

        query = TransportRequest.objects.filter(transport=transport_id)

        if accepted is not None:
            if accepted.lower() == 'true':
                # Must include those which are inside of campaign of which transport was found
                query = query.filter(accepted_by_driver=True)
            elif accepted.lower() == 'false':
                query = query.filter(transport_found=False).filter(accepted_by_driver=False)

        return query

    def perform_create(self, serializer: BaseSerializer) -> None:
        user = self.request.user
        start_and_end = parse_start_and_end_location(serializer)

        transport_request = serializer.save(start_location=start_and_end['start_location'], end_location=start_and_end['end_location'], passenger=user)
        send_transport_request_received_message(user.id, serializer.validated_data['transport'].driver.id, serializer.validated_data['transport'].id, transport_request.id)


class MyActiveTransportRequestsViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = TransportRequestWithTransportInfoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet:
        return TransportRequest.objects\
            .filter(passenger=self.request.user.id)\
            .exclude(transport_found=True, accepted_by_driver=False)\
            .order_by('transport_found', '-created_at')
#             TODO: make sure ordering works, those which transport was found must appear before
# those for which it wasnt. IN these 2 groups must be ordered by created at


class TransportRequestsOfCampaignViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = TransportRequestWithTransportInfoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet:
        campaign_id = int(self.request.query_params.get('campaign_id', None))
        if self.request.user.id != get_object_or_404(Campaign, pk=campaign_id).owner.id:
            raise PermissionDenied()

        return TransportRequest.objects.filter(inside_campaign=campaign_id)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def accept_passengers_request(request):
    transport_request_id = int(request.query_params.get('transport_request', None))
    transport_request_in_db = TransportRequest.objects.get(id=transport_request_id)

    try:
        c_in_db = Campaign.objects.get(id=transport_request_in_db.inside_campaign.id)
    except:
        c_in_db = None

    if not transport_request_in_db.transport.driver.id == request.user.id:
        raise PermissionDenied()

    if c_in_db:
        c_in_db.transport_was_found = True
        c_in_db.save()

    transport_request_in_db.accepted_by_driver = True
    transport_request_in_db.transport_found = True
    transport_request_in_db.save()

    transport_request_accepted_message(transport_request_in_db.transport.driver, transport_request_in_db.passenger, transport_request_in_db)
    if transport_request_in_db.transport.get_still_available_seats() == 0:
        transport_found_all_passengers_message(transport_request_in_db.transport, TransportRequest.objects.filter(transport=transport_request_in_db.transport, accepted_by_driver=False))

    return Response(status=status.HTTP_204_NO_CONTENT)

