# Generated by Django 4.2.3 on 2023-08-03 13:38

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0005_book_book_reviews_alter_review_book_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='full_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='author',
            name='bio',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='author',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='author',
            name='first_name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='author',
            name='last_name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='author',
            name='pic',
            field=models.ImageField(blank=True, upload_to='book/author/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='author',
            name='slug',
            field=models.SlugField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='author',
            name='website',
            field=models.URLField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='ISBN',
            field=models.CharField(blank=True, max_length=13, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='book_reviews',
            field=models.PositiveIntegerField(blank=True, default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AlterField(
            model_name='book',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='books_category', to='book.category'),
        ),
        migrations.AlterField(
            model_name='book',
            name='condition',
            field=models.CharField(blank=True, choices=[('New', 'New'), ('Old', 'Old')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='cover_image',
            field=models.FileField(blank=True, upload_to='book/cover_image/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='book',
            name='num_pages',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='page_image',
            field=models.FileField(blank=True, upload_to='book/page_image/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='book',
            name='publish_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='stock',
            field=models.CharField(blank=True, choices=[('In Stock', 'In Stock'), ('Out Of Stock', 'Out Of Stock')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to='book/category/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='publisher',
            name='address',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='publisher',
            name='social_twitter',
            field=models.URLField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='publisher',
            name='website',
            field=models.URLField(blank=True, max_length=255, null=True),
        ),
    ]