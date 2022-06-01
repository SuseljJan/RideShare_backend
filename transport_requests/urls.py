from django.urls import include, path
from rest_framework.routers import DefaultRouter

from transport_requests import views
router = DefaultRouter()

router.register(r'', views.TransportRequestViewSet, basename='TransportRequest')
# previously /transport/taken
# !! need to know if they were accepted, are they yet pending acceptings
router.register(r'my/active', views.MyActiveTransportRequestsViewSet, basename='MyActiveTransportRequests')

# previously /campaign/requests_of
router.register(r'of_campaign', views.TransportRequestsOfCampaignViewSet, basename='TransportRequestsOfCampaign')


urlpatterns = [
    # Driver accepts request from passenger - query params: offer_from_passenger (id)
    # previously /transport/accept_transport_request
    path('accept/', views.accept_passengers_request),
    path('', include(router.urls)),
]