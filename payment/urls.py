from django.urls import path
from .views import *

urlpatterns = [
    path('hello/', HelloWorldView.as_view(), name='hello'),
    path('payment/', CreatePaymentView.as_view(), name='payment'),
    path('payment/execute', ExecutePaymentView.as_view(), name='execute_payment'),
    path('payment/cancel', CancelPaymentView.as_view(), name='cancel_payment'),
]