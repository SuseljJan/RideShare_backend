import requests
from django.conf import settings
from django.template.loader import render_to_string
from requests.auth import HTTPBasicAuth

from user.models import User


def send_authenticated_message(sender_id, receiver_id, title, message):
    requests.post(f'{settings.MESSAGING_API_BASE_URI}/api/alert-messages/', json={
        'senderId':   sender_id,
        'receiverId': receiver_id,
        'title':      title,
        'message':    message
    }, auth=HTTPBasicAuth(settings.MESSAGING_API_USERNAME, settings.MESSAGING_API_PASSWORD))


def send_transport_request_received_message(sender_id, receiver_id, transport_id, transport_request_id):
    requests.post(f'{settings.MESSAGING_API_BASE_URI}/api/alert-messages/', json={
        'senderId': sender_id,
        'receiverId': receiver_id,
        'title': 'NEW TRANSPORT REQUEST',
        'message': render_to_string(
            'messaging/transport_request_received.html', {
                'sender_username': User.objects.get(id=sender_id).username,
                'transport_requests_link': f'{settings.FRONTENT_BASE_URI}/me/transport/{transport_id}/requests?highlightRequest={transport_request_id}'
            })
    }, auth=HTTPBasicAuth(settings.MESSAGING_API_USERNAME, settings.MESSAGING_API_PASSWORD))


def transport_request_accepted_message(driver_obj, passenger_obj, transport_request_obj):
    send_authenticated_message(
        driver_obj.id,
        passenger_obj.id,
        'TRANSPORT REQUEST ACCEPTED',
        render_to_string(
            'messaging/transport_request_accepted.html', {
                'driver_username': driver_obj.username,
                'transport_requests_link': f'{settings.FRONTENT_BASE_URI}/me/transports?highlightTaken={transport_request_obj.id}'
            }
        )
    )


def transport_found_all_passengers_message(transport, transport_requests):
    for tr_request in transport_requests:
        send_authenticated_message(
            transport.driver.id,
            tr_request.passenger.id,
            'PASSENGERS FOR TRANSPORT FOUND',
            render_to_string(
                'messaging/transport_found_passengers.html', {
                    'driver_username': transport.driver.username
                }
            )
        )
