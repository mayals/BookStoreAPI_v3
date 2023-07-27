from rest_framework import serializers
from.models import Category, Publisher, Author, Tag, Review, Book



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'icon', 'created_at']



class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['id','name', 'slug',  'address', 'website', 'created_at', 'updated_at']



class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'first_name', 'last_name', 'slug', 'email', 'bio', 'pic', 'website', 'created_at', 'updated_at']




class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']



class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'book', 'user', 'integerRating', 'textRating', 'created_at', 'updated_at']



class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'ISBN', 'title', 'slug', 'category', 'publishers', 'authors', 'tags','average_rating',
                  'publish_date', 'num_pages', 'cover_image', 'page_image', 'condition', 'stock', 'created_at', 'updated_at'
                ]




