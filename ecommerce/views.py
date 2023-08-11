from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, generics, response, validators, status
from .models import Order, OrderBook
from book.models import Book
from .serializers import OrderSerializer,OrderBookSerializer
from django.utils import timezone

class OrderViewSet(viewsets.ModelViewSet):
    queryset= Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
 

class OrderCreateAPIView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):   
        order = Order.objects.filter(user=self.request.user)
        if not order.exists():
            ## NEW ORDER ##    
                                  #  Order fields = ['id', 'user', 'order_date', 'status',
                                  #'total_amount', 'city', 'zip_code', 'street', 'state',
                                  #'country', 'phone_no', 'payment_status', 'payment_mode',  
                                  #'orderbooks', # related_field -- come from OrderBook model  
            data = self.rquest.data                     
            orderbooks = self.request.data['orderbooks']  #this data come  from related field orderbooks fom anothe model OrderBook
            
            if orderbooks and len(orderbooks) == 0:
                return response.Response({'error': 'No order recieved'},status=status.HTTP_400_BAD_REQUEST)
            else:
                for item in orderbooks:
                    total_amount = sum( item['price'] * item['quantity'] ) #'price' #'quantity' fields come from the related field orderbooks
  
                # CREATE NEW ORDER #                   
                order = Order.objects.create(
                                        user         = self.request.user,
                                        order_date   = timezone.now(),
                                        city         = self.rquest.data['city'],
                                        zip_code     = self.rquest.data['zip_code'],
                                        street       = self.rquest.data['street'],
                                        phone_no     = self.rquest.data['phone_no'],
                                        country      = self.rquest.data['country'],
                                        total_amount = total_amount
                )



                # CREATE NEW orderbook THAT CONTAIN order FIELD #
                orderbooks = self.request.data['orderbooks']
                for item in orderbooks:
                    book = Book.objects.get(id = item['book']) # 'book'=  value of book id come from related field orderbooks that come from OrderBook model
                    book_title = book.title 
                    orderbook = OrderBook.objects.create(
                                                        book= book,
                                                        order = order, # the order we created above 
                                                        quantity = item['quantity'],# 'quantity'=  value of quantity come from related field orderbooks that come from OrderBook model
                                                        price = item['price'],# 'price'=  value of 'price' come from related field orderbooks that come from OrderBook model
                                                        book_title = book_title,
                    )
                
                serializer = OrderSerializer(order, many=False)
                return response.Response(serializer.data, status=status.HTTP_201_CREATED)
                
        return response.Response({"IntegrityError": "This user already has order"},status=status.HTTP_400_BAD_REQUEST)
            
        




        
         # https://docs.djangoproject.com/en/4.2/topics/db/queries/#making-queries
            # https://stackoverflow.com/questions/50015204/direct-assignment-to-the-forward-side-of-a-many-to-many-set-is-prohibited-use-e
        # old order 
        # order =  Order.objects.filter(user=self.request.user)
            #raise validators.ValidationError({"IntegrityError": "This user has already order"},)
            
            
            # def get_serializer_context(self):
            #     print(super().get_serializer_context())
                 # Assuming you have user authentication
           
           
           
            # Ensure there is only one open order for request user 
            # if not Order.objects.filter(user=self.request.user).exists():    
            #     serializer.save(user=self.request.user) # here we open a new order for this user
            #     book_id = self.kwargs.get('book_id')
            #     book = Book.objects.get(Book, pk=book_id)
            #     user = self.request.user 
            #     order = Order.objects.create(user=user)
            #     order.books = order.add(book)
            #     order.save()
            #     serializer = self.serializer_classs(queryset=order,many=False) 
            #     serializer.save()
            #     return serializer.data
            # serializer.save(user=self.request.user)
            # old_order = get_object_or_404(Order,user=self.request.user)
            # old_books= old_order.books.all()
            # new_book = Book.objects.get(Book, pk=book_id)
            # books = old_books.add(new_book)
            # serializer.save(user=user, books=books)     # book.reviews_count+= 1
            # return response.Response(serializer.data, status=status.HTTP_201_CREATED)
            # else:   #unique_together = ("user", "book") in models.Rview
            # raise validators.ValidationError({"IntegrityError": "This user already has order"},)