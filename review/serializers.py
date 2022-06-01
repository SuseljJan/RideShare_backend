from rest_framework import serializers

from review.models import Review
from user.models import User
from user.serializers import UserSerializer, GenericUserSerializer

class MyReviewsSerializer(serializers.ModelSerializer):
    reviewer = GenericUserSerializer()

    class Meta:
        model = Review
        exclude = ['reviewed']

class ReviewSerializer(serializers.ModelSerializer):
    reviewed = UserSerializer()
    reviewer = UserSerializer()

    class Meta:
        model = Review
        fields = '__all__'


class CreateReviewSerializer(serializers.ModelSerializer):
    reviewer = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'

    def create(self, validated_data):
        validated_data.update({
            'reviewer': self.context['request'].user
        })
        return Review.objects.create(**validated_data)




