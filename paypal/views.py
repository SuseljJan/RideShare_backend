from django.shortcuts import render
from rest_framework import response, status
from rest_framework.decorators import api_view
import paypalrestsdk
from rest_framework.response import Response
from paypalrestsdk import Payout, ResourceNotFound


from transport.models import Transport
from user.models import User
from datetime import datetime

#
# @api_view(['POST'])
# def payWithBL(request):
#     serializer = PayWithPayPalSerializerWithBL(data=request.data)
#     if not serializer.is_valid():
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     ofp = PassengerSOffer.objects.get(id=serializer.validated_data['offer_from_passenger'])
#
#     thp = TransportHasPassengers.objects.get(offer_from_passenger=ofp.id)
#     thp.has_been_paid_for = True
#     thp.save()
#
#     return Response(pay(ofp.price, serializer.validated_data['return_url'], serializer.validated_data['cancel_url']))
#
#
# def pay(price, return_url, cancel_url):
#
#     valid_price = str(round(float(price), 2))
#
#
#     paypalrestsdk.configure({
#         "mode":          "sandbox",  # sandbox or live
#         "client_id":     "AY5B8sjXs8lyps6rPaeRnijQb-ODaJSFXL9957wfK2K4O6lsO-DMy_hrh7SrMysxeH1pb4ICasFAskt8",
#         "client_secret": "EEzM4LKeh-Oa_vVoMCru48IPmbWJBevsiQ2s4mbl75nyDMXYjuM7HJe8BVi5Y0m5KokRgFc6IFJNg3Er"})
#
#     payment = paypalrestsdk.Payment({
#         "intent":        "sale",
#         "payer":         {
#             "payment_method": "paypal"},
#         "redirect_urls": {
#             "return_url": return_url,
#             "cancel_url": cancel_url},
#         "transactions":  [{
#             "item_list":   {
#                 "items": [{
#                     "name":     "Shared transportation",
#                     "sku":      "item",
#                     "price":    valid_price,
#                     "currency": "EUR",
#                     "quantity": 1}]},
#             "amount":      {
#                 "total":    valid_price,
#                 "currency": "EUR"},
#             "description": "This is the payment transaction description."}]})
#
#     if payment.create():
#         for link in payment.links:
#             if link.rel == "approval_url":
#                 # Convert to str to avoid Google App Engine Unicode issue
#                 # https://github.com/paypal/rest-api-sdk-python/pull/58
#                return str(link.href)
#     else:
#         return payment.error
#
# @api_view(['POST'])
# def success(request):
#     paypalrestsdk.configure({
#         "mode":          "sandbox",  # sandbox or live
#         "client_id":     "AY5B8sjXs8lyps6rPaeRnijQb-ODaJSFXL9957wfK2K4O6lsO-DMy_hrh7SrMysxeH1pb4ICasFAskt8",
#         "client_secret": "EEzM4LKeh-Oa_vVoMCru48IPmbWJBevsiQ2s4mbl75nyDMXYjuM7HJe8BVi5Y0m5KokRgFc6IFJNg3Er"})
#
#     payerId = request.query_params.get('PayerID', None)
#     paymentId = request.query_params.get('paymentId', None)
#
#     offer_from_passenger = PassengerSOffer.objects.get(id=request.query_params.get('offer_from_passenger', None))
#     thp = TransportHasPassengers.objects.get(offer_from_passenger=offer_from_passenger.id)
#     transport = Transport.objects.get(id=thp.transport.id)
#     driver = User.objects.get(id=transport.driver.id)
#
#     payment = paypalrestsdk.Payment.find(paymentId)
#     if payment.execute({"payer_id": payerId}):
#         price = payment.transactions[0].amount.total
#         paypals_cut = payment.transactions[0].related_resources[0].sale.transaction_fee.value
#
#         payout(driver.email, (float(price)-float(paypals_cut)))
#
#         return Response(True)
#     else:
#         breakpoint()
#         return Response(payment.error, status=status.HTTP_400_BAD_REQUEST)
#
#
# def payout(receiver, amount):
#     paypalrestsdk.configure({
#         "mode":          "sandbox",  # sandbox or live
#         "client_id":     "AY5B8sjXs8lyps6rPaeRnijQb-ODaJSFXL9957wfK2K4O6lsO-DMy_hrh7SrMysxeH1pb4ICasFAskt8",
#         "client_secret": "EEzM4LKeh-Oa_vVoMCru48IPmbWJBevsiQ2s4mbl75nyDMXYjuM7HJe8BVi5Y0m5KokRgFc6IFJNg3Er"})
#
#     payout = Payout({
#         "sender_batch_header": {
#             "sender_batch_id": str(datetime.now()),
#             "email_subject":   "You have a payment"
#         },
#         "items":               [
#             {
#                 "recipient_type": "EMAIL",
#                 "amount":         {
#                     "value":    amount,
#                     "currency": "EUR"
#                 },
#                 "receiver":       receiver,
#                 "note":           "Thank you.",
#                 "sender_item_id": "item_1"
#             }
#         ]
#     })
#     if payout.create(sync_mode=False):
#         return payout.batch_header.payout_batch_id
#     else:
#         return payout.error