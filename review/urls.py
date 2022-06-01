from django.urls import path, include
from rest_framework.routers import DefaultRouter

from review import views

router = DefaultRouter()
router.register(r'create', views.CreateReviewViewSet)
router.register(r'mine', views.MyReviews, basename='my_reviews')


urlpatterns = [
    path('', include(router.urls)),
]
