from rest_framework.views import APIView
from rest_framework.response import Response
import paypalrestsdk
from paypalrestsdk import Payment, configure
from rest_framework import status
from django.conf import settings

from .models import PayPalPayment
from .serializer import PayPalPaymentSerializer

paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE, # "sandbox" or "live"
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET
})

class HelloWorldView(APIView):
    def get(self, request):
        return Response({"message": "Hello, world!"})
    
class CreatePaymentView(APIView):
    def post(self, request):
        # Create the payment object
        payment = Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "redirect_urls": {
                "return_url": "http://localhost:8000/payment/execute",
                "cancel_url": "http://localhost:8000/payment/cancel"
            },
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": "item",
                        "sku": "item",
                        "price": "5.00",
                        "currency": "USD",
                        "quantity": 1
                    }]
                },
                "amount": {
                    "total": "5.00",
                    "currency": "USD"
                },
                "description": "This is the payment description."
            }]
        })

        # Create the payment
        if payment.create():
            print("Payment created successfully")
        else:
            print(payment.error)

        # Save the payment in the database
        # Create the payment in the database and assign it to a variable
        payment_instance = PayPalPayment.objects.create(
            transaction_id=payment.id,
            amount=payment.transactions[0].amount.total,
            currency=payment.transactions[0].amount.currency,
            status=payment.state,
        )

        # Serialize the payment instance
        serializer = PayPalPaymentSerializer(payment_instance)

        # Return the serialized payment instance
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ExecutePaymentView(APIView):
    def get(self, request):
        # Here you would typically finalize the payment and update your application's state.
        # For now, let's just return a success message.
        return Response({"message": "Payment executed successfully"})

class CancelPaymentView(APIView):
    def get(self, request):
        # Here you would typically handle a cancelled payment.
        # For now, let's just return a cancellation message.
        return Response({"message": "Payment cancelled"}, status=status.HTTP_200_OK)
    
class CreateCardPaymentView(APIView):
    def post(self, request):
        # Create the credit card object
        card = {
            "type": request.data.get('type'),
            "number": request.data.get('number'),
            "expire_month": request.data.get('expire_month'),
            "expire_year": request.data.get('expire_year'),
            "cvv2": request.data.get('cvv2'),
            "first_name": request.data.get('first_name'),
            "last_name": request.data.get('last_name')
        }

        # Create the payment object
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "credit_card",
                "funding_instruments": [{
                    "credit_card": card
                }]
            },
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": "item",
                        "sku": "item",
                        "price": "5.00",
                        "currency": "USD",
                        "quantity": 1
                    }]
                },
                "amount": {
                    "total": "5.00",
                    "currency": "USD"
                },
                "description": "This is the payment description."
            }]
        })

        # Create the payment
        if payment.create():
            # The payment has been created successfully
            # Here you can add your logic to update your application's state
            return Response({"message": "Payment created successfully"},status=status.HTTP_201_CREATED)
        else:
            # The payment creation was not successful
            return Response({"error": "Payment creation failed"}, status=status.HTTP_200_OK)