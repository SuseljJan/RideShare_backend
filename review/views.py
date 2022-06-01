from django.db.models import QuerySet
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from review.models import Review
from review.serializers import CreateReviewSerializer, MyReviewsSerializer


class CreateReviewViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Review.objects.all()
    serializer_class = CreateReviewSerializer
    permission_classes = [IsAuthenticated]


class MyReviews(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = MyReviewsSerializer

    def get_queryset(self) -> QuerySet:
        return Review.objects.filter(reviewed=self.request.user)
