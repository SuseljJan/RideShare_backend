from django.urls import include, path
from rest_framework.routers import DefaultRouter

from user import views
from user.views import about_me

router = DefaultRouter()

router.register(r'with_reviews', views.UserViewSet)
router.register(r'', views.GenericUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('about_me', about_me)
]