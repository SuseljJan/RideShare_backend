from django.db.models import QuerySet
from rest_framework import status, viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import BaseSerializer

from campaign.models import Campaign
from campaign.serializers import CampaignSerializer


class ActiveCampaignViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = CampaignSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet:
        return Campaign.objects.filter(
            owner=self.request.user.id,
            transport_was_found=False
        )


class AllCampaignsViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    serializer_class = CampaignSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        campaign_obj = super().get_object()
        if campaign_obj.owner.id != self.request.user.id:
            raise PermissionError()
        return campaign_obj

    def get_queryset(self) -> QuerySet:
        return Campaign.objects.filter(
            owner=self.request.user.id,
        ).order_by('created_at')

    def perform_create(self, serializer: BaseSerializer) -> None:
        user = self.request.user
        serializer.save(owner=user)


class NonPaginatedCampaignsViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = CampaignSerializer
    pagination_class = None
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet:
        active = self.request.query_params.get('active', 'ALL')
        user_id = self.request.user.id
        if active.lower() == 'true':
            return Campaign.objects.filter(owner=user_id, transport_was_found=False)
        elif active.lower() == 'false':
            return Campaign.objects.filter(owner=user_id, transport_was_found=True)
        else:
            return Campaign.objects.filter(owner=user_id)
