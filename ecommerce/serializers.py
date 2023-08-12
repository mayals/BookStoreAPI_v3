from rest_framework import serializers
from.models import Book, OrderBook, Order, Cart, Payment
from book.serializers import BookSerializer



class OrderBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderBook
        fields = ['id','order', 'book', 'quantity', 'price' ,'book_title']
    extra_kwargs = {
                    'id'        : {'read_only': True },
                    'order'     : {'read_only': True },          
                    'book'      : {'required': True },
                    'book_title': {'required': False },
        }


class OrderSerializer(serializers.ModelSerializer):
    orderbooks = serializers.SerializerMethodField(method_name="get_orderbooks",read_only=True)      # related_field--  must be read only true
    class Meta:
        model = Order
        fields = ['id', 'user', 'order_date', 'status',
                  'total_amount', 'city', 'zip_code', 'street', 'state',
                  'country', 'phone_no', 'payment_status', 'payment_mode',  
                  'orderbooks', # related_field -- come from OrderBook model         
        ]

        extra_kwargs = {
                    'id'        : {'read_only': True },
                    'user'      : {'read_only': True }, # take user value from authentication         
                    'orderbooks': {'read_only': True } #, # related_field -- come from OrderBook model # MUST BE READ ONLY TRUE 
        } 
      
    @property
    def get_orderbooks(self): # obj --order
        orderbooks = OrderBook.objects.all().filter(order=self)
        
        return orderbooks
    
   



    
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'user', 'books']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'order', 'amount', 'is_paid', 'checkout_id', 'payment_date']