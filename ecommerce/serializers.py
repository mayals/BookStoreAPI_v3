from rest_framework import serializers
from.models import BookOrdering, Order, Cart, Payment


class BookOrderingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookOrdering
        fields = ['id', 'Book', 'order', 'bookQuantity', 'bookPrice']



class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookOrdering
        fields = ['id', 'user', 'books', 'order_date', 'total_quantity', 'status']


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'user', 'books']


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'order', 'amount', 'is_paid', 'checkout_id', 'payment_date']