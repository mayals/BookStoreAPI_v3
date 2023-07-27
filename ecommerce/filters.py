import django_filters
from .models import Order


class OrderFilter(django_filters.FilterSet):
    Order_date = django_filters.DateFromToRangeFilter(field_name='Order_date')
       

    class Meta:
        model = Order
        fields = ['enrollment_date']
