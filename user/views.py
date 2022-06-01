from django.db.models import Avg, F, Count
from rest_framework import viewsets, mixins
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from review.models import Review
from review.serializers import ReviewSerializer, MyReviewsSerializer
from user.models import User
from user.serializers import UserSerializer, GenericUserSerializer, UserSerializerForTransportList


class UserViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        return super()\
            .get_queryset()\
            .annotate(avg_rating=Avg(F('reviewed__number_of_stars')))\
            .annotate(number_of_ratings=Count(F('reviewed')))


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def about_me(request):
    serializer = GenericUserSerializer(request.user)
    return Response(serializer.data)


class GenericUserViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializerForTransportList

    def get_object(self):
        user = super().get_object()
        my_reviews = Review.objects.filter(reviewed=user)

        user.avg_rating = my_reviews.aggregate(Avg('number_of_stars'))['number_of_stars__avg']
        user.number_of_ratings = my_reviews.count()

        return user

    @action(detail=True, methods=['GET'])
    def latest_reviews(self, request, *args, **kwargs):
        user = self.get_object()
        reviews_of_user = Review.objects\
            .filter(reviewed=user).order_by('-created_at')

        page = self.paginate_queryset(reviews_of_user)

        if page is not None:
            serializer = MyReviewsSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = MyReviewsSerializer(reviews_of_user.limit(5), many=True)
        return Response(serializer.data)

