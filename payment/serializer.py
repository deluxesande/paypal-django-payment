from rest_framework import serializers
from .models import PayPalPayment

class PayPalPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayPalPayment
        fields = ['id', 'transaction_id', 'amount', 'currency', 'status', 'created_at']
        read_only_fields = ['status', 'created_at']   