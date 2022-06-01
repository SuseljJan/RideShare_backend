from django.urls import include, path
from rest_framework.routers import DefaultRouter

from location import views

router = DefaultRouter()

router.register(r'users_often_used', views.OftenUsedLocationViewSet, basename='often_used_locations')
router.register(r'users_often_used_all', views.OftenUsedLocationsNotPaginatedViewSet, basename='all_often_used')

urlpatterns = [
    path('', include(router.urls)),
]