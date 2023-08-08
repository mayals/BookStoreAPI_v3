from rest_framework import serializers
from.models import Book, BookOrdering, Order, Cart, Payment
from book.serializers import BookSerializer

class BookOrderingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookOrdering
        fields = ['id', 'Book', 'order', 'bookQuantity', 'bookPrice']



class OrderSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    books = BookSerializer(required=False, read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'user', 'books', 'order_date', 'total_quantity', 'status']

    def get_user(self):
        return self.request.user




    
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'user', 'books']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'order', 'amount', 'is_paid', 'checkout_id', 'payment_date']