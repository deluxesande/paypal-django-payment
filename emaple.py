import paypalrestsdk

from rest_framework.views import APIView
from rest_framework.response import Response

class ProcessPayment(APIView):
    def post(self, request, *args, **kwargs):
        # Set up the PayPal client
        paypalrestsdk.configure({
            "mode": "sandbox",  # sandbox or live
            "client_id": "YOUR_CLIENT_ID",
            "client_secret": "YOUR_CLIENT_SECRET"
        })

        # Create a new payment
        payment = paypalrestsdk.Payment({
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

        # Create the payment and redirect the user
        if payment.create():
            for link in payment.links:
                if link.method == "REDIRECT":
                    # Capture the url
                    redirect_url = str(link.href)
                    return Response({"redirect_url": redirect_url})
        else:
            return Response({"error": payment.error}, status=400)