from django.urls import path, include
from rest_framework.routers import DefaultRouter
from alert_messages import views


router = DefaultRouter()
router.register(r'', views.AlertMessagesViewSet, basename='AlertMessage')

urlpatterns = [
    path('archive/<int:message_id>/', views.archive_message),
    path('read/<int:message_id>/', views.read_message),
    path('', include(router.urls))
]