from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import Category, Publisher, Author, Tag, Review, Book
from rest_framework.validators import UniqueValidator


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100,validators=[UniqueValidator(queryset=Category.objects.all())]    
)
    def validate_name(self, value):
        if value is None:
            raise serializers.ValidationError('This field is required') 
        if Category.objects.filter(name=value).exists():
            raise serializers.ValidationError("category name's must be unique")     
        print(value)
        return  value
      
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'icon', 'created_at','category_books']
        extra_kwargs = {
                    'name' : {'required' : True },
                    'id'   : {'read_only': True },
                    'slug' : {'read_only': True },
                    'category_books':{'read_only': True },
        }




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




