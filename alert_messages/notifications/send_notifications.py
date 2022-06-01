from alert_messages.models import Message


def notify_driver_about_accepted_offer(driver, passenger):
    Message.objects.create(
        receiver=driver,
        message=passenger.email + ' has sent a request to your ride offer'
    )


def notify_passenger_about_his_accepted_offer(driver, passenger):
    msg = Message.objects.create(
        receiver=passenger,
        message='Your request for a ride with ' + driver.email + ' was accepted'
    )

