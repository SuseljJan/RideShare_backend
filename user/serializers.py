from rest_framework import serializers
from review.models import Review
from user.models import User


class UserSerializerForCampaigns(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']


class GenericUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class GenericReviewSerializer(serializers.ModelSerializer):
    reviewer = GenericUserSerializer()

    class Meta:
        model = Review
        fields = '__all__'


class UserSerializerForTransportList(serializers.ModelSerializer):
    avg_rating = serializers.FloatField(read_only=True)
    number_of_ratings = serializers.FloatField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'avg_rating', 'number_of_ratings']


class UserSerializer(serializers.ModelSerializer):
    reviewed = GenericReviewSerializer(many=True)
    avg_rating = serializers.FloatField(read_only=True)
    number_of_ratings = serializers.FloatField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'reviewed', 'avg_rating', 'number_of_ratings']
