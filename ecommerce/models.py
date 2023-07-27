from django.db import models
from django.urls import reverse
from django.conf import settings
from book.models import Book
# https://pypi.org/project/shortuuid/
from shortuuid.django_fields import ShortUUIDField 

 
class BookOrdering(models.Model):
    id              = ShortUUIDField(primary_key=True, unique=True, length=6, max_length=6, editable=False)
    book            = models.ForeignKey('book.Book', on_delete=models.CASCADE,  null=True , blank=False, related_name='book_orders')
    order           = models.ForeignKey('Order', on_delete=models.CASCADE, null=True , blank=False, related_name='order_books')
    bookQuantity    = models.PositiveIntegerField(default=0)
    bookPrice       = models.DecimalField(max_digits=10, decimal_places=2)
      
    def __str__(self):
            return f"Book ordering by {self.order.user.email} on {self.bookQuantity} x {self.book.title} in Order #{self.order.order_id}"
           



class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]

    id             = ShortUUIDField(primary_key=True, unique=True, length=6, max_length=6, editable=False)
    user           = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True , blank=False, related_name='user_orders')
    books          = models.ManyToManyField('book.Book',through='BookOrdering') 
    order_date     = models.DateTimeField(auto_now_add=True, auto_now=False)   
    total_quantity = models.DecimalField(max_digits=10, decimal_places=2)
    status         = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    # shipping_address = models.TextField()
    # payment_method  = models.CharField(max_length = 20)
    # shipping_method = models.ForeignKey(ShippingMethod, on_delete=models.CASCADE, null=True , blank=False, related_name='orders')
    def __str__(self):
        return f"Order #{self.id}     belong to customer:{self.order.user.email}"
    
    def get_absolute_url(self):
        return reverse('order-detail', kwargs = {'id':self.id})      #vue view_name='{model_name}-detail'
    
    def get_order_books(self):
        return self.BookOrdering_set.all()
    
    def get_total_quantity(self):
        total_quantity = 0
        order_books = self.get_order_books()
        for item in order_books:
            total_quantity += item.bookQuantity
        return total_quantity

    def get_total_price(self):
        total_price = 0.0
        order_books = self.get_order_books()
        for item in order_books:
            total_price += item.bookPrice * item.bookQuantity
        return total_price
    
    class Meta:
        ordering = ('order_date',)
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

   

   
class Cart(models.Model): 
    id       = ShortUUIDField(primary_key=True, unique=True, length=6, max_length=6, editable=False)
    user     = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=False, related_name='cart') 
    books    = models.ManyToManyField(Book)    
 
    def __str__(self):
        return str(self.user.email)





class Payment(models.Model):
    id = ShortUUIDField(primary_key=True, unique=True, length=6, max_length=6, editable=False )
    order= models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orders')
    amount = models.FloatField(null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    checkout_id = models.CharField(max_length=500)
    payment_date = models.DateTimeField(auto_now_add=True)