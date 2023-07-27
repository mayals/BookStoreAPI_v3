# Generated by Django 4.2.3 on 2023-07-25 14:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import shortuuid.django_fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('book', '0002_alter_book_authors_alter_book_publisher_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BookOrdering',
            fields=[
                ('id', shortuuid.django_fields.ShortUUIDField(alphabet=None, editable=False, length=6, max_length=6, prefix='', primary_key=True, serialize=False, unique=True)),
                ('bookQuantity', models.PositiveIntegerField(default=0)),
                ('bookPrice', models.DecimalField(decimal_places=2, max_digits=10)),
                ('book', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='book_orders', to='book.book')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', shortuuid.django_fields.ShortUUIDField(alphabet=None, editable=False, length=6, max_length=6, prefix='', primary_key=True, serialize=False, unique=True)),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('total_quantity', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('PROCESSING', 'Processing'), ('SHIPPED', 'Shipped'), ('DELIVERED', 'Delivered'), ('CANCELLED', 'Cancelled')], default='PENDING', max_length=20)),
                ('books', models.ManyToManyField(through='ecommerce.BookOrdering', to='book.book')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_orders', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
                'ordering': ('order_date',),
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', shortuuid.django_fields.ShortUUIDField(alphabet=None, editable=False, length=6, max_length=6, prefix='', primary_key=True, serialize=False, unique=True)),
                ('books', models.ManyToManyField(to='book.book')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cart', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='bookordering',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_books', to='ecommerce.order'),
        ),
    ]
