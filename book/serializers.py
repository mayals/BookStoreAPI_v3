from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import Category, Publisher, Author, Tag, Review, Book
from rest_framework.validators import UniqueValidator
from . import validators as CustomValidator
from urllib.parse import urlparse

class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100,validators=[UniqueValidator(queryset=Category.objects.all())])    
    
    def validate_name(self, value):
        if value is None:
            raise serializers.ValidationError('This field is required') 
        if Category.objects.filter(name=value).exists():
            raise serializers.ValidationError("category name's must be unique")     
        print(value)
        return  value
      
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'icon', 'created_at']
        extra_kwargs = {
                    'name' : {'required' : True },
                    'id'   : {'read_only': True },
                    'slug' : {'read_only': True },
                   
        }




class PublisherSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100,required=True,validators=[UniqueValidator(queryset=Publisher.objects.all())] ) 
    social_twitter = serializers.URLField(required=False,validators=[CustomValidator.validate_hostname('twitter.com', 'www.twitter.com')])

    def validate_name(self, value):
        if value is None:
            raise serializers.ValidationError('This field is required') 
        if Publisher.objects.filter(name=value).exists():
            raise serializers.ValidationError("Publisher name's must be unique")     
        return  value
    
    def validate_social_twitter(self, value): 
        if value is not None:
            hostnames = set(hostnames)
            try:
                result = urlparse(value)
                if result.hostname not in hostnames:
                    serializers.ValidationError(f'The hostname {result.hostname} is not allowed.')
            except ValueError:
                raise serializers.ValidationError('invalid url')
        return  value       
        
    def validate_website(value):
        obj = urlparse(value)
        if 'com' not in obj.hostname or 'www' not in obj.hostname :   # url.hostname     "www.example.com"
            raise serializers.ValidationError('please enter valid website url')

    
    class Meta:
        model = Publisher
        fields = ['id','name', 'slug', 'address', 'website','social_twitter', 'created_at', 'updated_at']
        extra_kwargs = {
                    'name' : {'required' : True },
                    'id'   : {'read_only': True },
                    'slug' : {'read_only': True },
                    'social_twitter' : {'required' : False },
                    'books': {'read_only': True },
        }      




  

class AuthorSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        return obj.get_author_fullname
    
    class Meta:
        model = Author
        fields = ['id', 'full_name', 'slug', 'first_name', 'last_name', 'email', 'bio', 'pic', 'website', 'created_at', 'updated_at']
        extra_kwargs = {
                    'name' : {'required' : True },
                    'id'   : {'read_only': True },
                    'slug' : {'read_only': True },
                    'pic' :  {'required' : False },
                    'books': {'read_only': True },
        } 



class TagSerializer(serializers.ModelSerializer):
    
    def validate_name(self, value):
        if value is None:
            raise serializers.ValidationError('This field is required') 
        if Tag.objects.filter(name=value).exists():
            raise serializers.ValidationError("tag name's must be unique")     
        print(value)
        return  value
      
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']
        extra_kwargs = {
                    'name' : {'required' : True },
                    'id'   : {'read_only': True },
                    'slug' : {'read_only': True },
        }
    






class ReviewSerializer(serializers.ModelSerializer):
    user  = serializers.StringRelatedField()  #  many reviewsunfo (ForignKey) -  to   - one user (primary key)
    book  = serializers.StringRelatedField()  #  many reviewsinfo (ForignKey) -  to   - one book (primary key)  
    class Meta:
        model = Review
        fields = ['id', 'user', 'book', 'number_rating', 'text_rating', 'created_at', 'updated_at']
        





class BookSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField() #   many books(ForignKey)  -  to   - one category(primary key)
    publishers = PublisherSerializer(many=True)  # Nested serialization
    authors = AuthorSerializer(many=True)  # Nested serialization
    tags = serializers.StringRelatedField(many=True, read_only=True)  # Nested serialization
    reviews = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'ISBN', 'title', 'slug', 'category', 'publishers', 'authors', 'tags','average_rating',
                  'publish_date', 'num_pages', 'cover_image', 'page_image', 'condition', 'stock', 'created_at', 'updated_at','reviews'
                ]
        extra_kwargs = {
                    'title' : {'required' : True },
                    'id'   : {'read_only': True },
                    'reviews' : {'read_only': True },
        } 


