from django.contrib import admin
from .models import BookOrdering, Order, Cart


@admin.register(BookOrdering)
class BookOrderingAdmin(admin.ModelAdmin):
    list_display = ['id', 'book', 'order', 'bookQuantity', 'bookPrice']
    list_filter = ['book', 'order', 'bookQuantity', 'bookPrice']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'order_date', 'total_quantity', 'status']
    list_filter = ['user', 'books', 'order_date', 'total_quantity', 'status']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']
    list_filter = ['user', 'books']
