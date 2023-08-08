from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, generics, response, validators, status
from .models import Order, BookOrdering
from book.models import Book
from .serializers import OrderSerializer
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
            instance = serializer.save(user=self.request.user)
            print('instance='+str(instance))
            book_id = self.kwargs.get('book_id')
            book = get_object_or_404(Book, id=book_id)
            bookordering = BookOrdering.objects.create(book=book)
            bookordering.order = instance
            bookordering.save()
            user = self.request.user
            if not Order.objects.filter(user=self.request.user).exists():    
                serializer.save(books=bookordering, user=self.request.user,order_date=timezone.now())
                return response.Response(serializer.data, status=status.HTTP_201_CREATED)
            else:   #unique_together = ("user", "book") in models.Rview
                raise validators.ValidationError({"IntegrityError": "This user has already order"},)
            
            
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
            raise validators.ValidationError({"IntegrityError": "This user already has order"},)