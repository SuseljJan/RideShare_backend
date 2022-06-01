from django.urls import path, include
from rest_framework.routers import DefaultRouter

from campaign import views

router = DefaultRouter()
router.register(r'active', views.ActiveCampaignViewSet, basename='active_campaign')
router.register(r'all', views.AllCampaignsViewSet, basename='all_campaigns')
# router.register(r'requests_of', views.RequestsOfCampaign, basename='requests_of_campaign')
router.register(r'non_paginated', views.NonPaginatedCampaignsViewSet, basename='non_paginated_campaigns')

urlpatterns = [
    path('', include(router.urls)),
]
