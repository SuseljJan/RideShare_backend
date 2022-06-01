from django.db.models import QuerySet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from alert_messages.models import Message
from alert_messages.serializers import MessageSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status, viewsets, mixins


class AlertMessagesViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet:
        return Message.objects\
            .filter(receiver=self.request.user.id, archived=False)\
            .order_by('read', '-posted')


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def read_message(request, message_id):
    searched_message: Message = Message.objects.get(id=message_id)

    if not searched_message.receiver.id == request.user.id:
        return Response(status=status.HTTP_403_FORBIDDEN)

    searched_message.read = True
    searched_message.save()
    return Response(True)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def archive_message(request, message_id):
    searched_message = Message.objects.get(id=message_id)

    if not searched_message.receiver.id == request.user.id:
        return Response(status=status.HTTP_403_FORBIDDEN)

    searched_message.archived = True
    searched_message.save()
    return Response(True)
