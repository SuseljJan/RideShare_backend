from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_details(request):
    return Response({
        'username': request.user.username
    })

@api_view(['GET'])
def test_view(request):
    return Response({'a': 1}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
