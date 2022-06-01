from django.urls import include, path
from rest_framework.routers import DefaultRouter

from transport import views

router = DefaultRouter()


# given transports of a specific user
router.register(r'given', views.GivenTransportsViewSet, basename='GivenTransports')


# negotiability added, can only be used for GET ../<id>
router.register(r'with_negotiability', views.TransportWithNegotiabilityViewSet, basename='WithNegotiability')
# all transports sorted by closest distance of SUM(start_location, end_location). See query params!
router.register(r'', views.TransportViewSet)

urlpatterns = [
    # Driver accepts request from passenger - query params: offer_from_passenger (id)
    path('cancel/<int:id>/', views.cancel_transport),
    path('', include(router.urls)),
]
