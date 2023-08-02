from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import Category, Publisher, Author, Tag, Review, Book
from rest_framework.validators import UniqueValidator
from . import validators as CustomValidator
from urllib.parse import urlparse

class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100,validators=[UniqueValidator(queryset=Category.objects.all())])    
    books_category = serializers.SerializerMethodField
    def validate_name(self, value):
        if value is None:
            raise serializers.ValidationError('This field is required') 
        if Category.objects.filter(name=value).exists():
            raise serializers.ValidationError("category name's must be unique")     
        print(value)
        return  value
    
    def get_books_category(self, obj):
        books_category = Book.category.all().filter(category=self)
        return books_category

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'icon', 'created_at','books_category']
        extra_kwargs = {
                    'name' :  {'required' : True },
                    'id'   :  {'read_only': True },
                    'slug' :  {'read_only': True },
                   'books_category':{'read_only':True},
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
    user  = serializers.StringRelatedField()  #  many reviews (ForignKey) -  to   - one user (primary key)
    book  = serializers.StringRelatedField()  #  many reviews (ForignKey) -  to   - one book (primary key)  
    class Meta:
        model = Review
        fields = ['id', 'user', 'book', 'rating_value', 'rating_text', 'created_at', 'updated_at']
        





class BookSerializer(serializers.ModelSerializer):
    title      = serializers.CharField(max_length=100,required=True) 
    # many to one field
    category   = serializers.SlugRelatedField(queryset = Category.objects.all(), slug_field = 'slug')  # to display category_id asredable  use name field  insead of id field                                                                                                           #   many books(ForignKey)  -  to   - one category(primary key)
    # many to many field
    publishers = PublisherSerializer(many=True) # Nested serialization
    authors    = AuthorSerializer(many=True) # Nested serialization
    tags       = TagSerializer(many=True)  # Nested serialization
    # related_field  read_only
    reviews    = serializers.SerializerMethodField

    class Meta:
        model = Book
        fields = ['id', 'ISBN', 'title', 'slug', 'category', 'publishers', 'authors', 'tags','average_rating','book_reviews',
                  'publish_date', 'num_pages', 'cover_image', 'page_image', 'condition', 'stock', 'created_at', 'updated_at','reviews'
                ]
        extra_kwargs = {
                    'id'          : {'read_only': True },
                    'title'       : {'required' : True },
                    
                    'category'    : {'required' : True },
                    
                    'authors'      : {'required' : True },
                    'tags'         : {'required' : True },
                    'publishers'   : {'required' : True },
                    
                    'cover_image' : {'required' : False},
                    'page_image'  : {'required' : False},
                    'reviews'     : {'read_only': True }, # related_field
        } 

    #reviews  related_field  read_only
    def get_reviews(self):
        reviews = Review.objects.all().filter(book=self)
        return reviews
    
    

    
    def create(self, validated_data):
        publishers_data = validated_data.pop('publishers')
        authors_data = validated_data.pop('authors')
        tags_data = validated_data.pop('tags')
        
        book = Book.objects.create(**validated_data)
        
        for publisher_data in publishers_data:
            publisher, created_publisher= Publisher.objects.get_or_create(**publisher_data)
            book.publishers.add(publisher)
            print(publishers_data)
           
        for author_data in authors_data:
            author, created_author= Author.objects.get_or_create(**author_data)
            book.authors.add(author)
            print(authors_data)
        for tag_data in tags_data:
            tag, created_tag= Tag.objects.get_or_create(**tag_data)
            book.tags.add(tag)
            tags_data
        return book
    
    
    
    # def create(self, validated_data):
    #     publishers_data = validated_data.pop('publishers')
    #     book = Book.objects.create(**validated_data)
    #     for data in publishers_data:
    #         room, created = Rooms.objects.get_or_create(**data)
    #         module.rooms.add(room)
    #     return module
    
    


    # def create(self, validated_data): # work ok :)
    #     book = Book(
    #                 title       = validated_data.get('title') ,  # any title , must be unique
    #                 category    = validated_data.get('category') , # this field choicen from categories list 
    #                 publishers  = validated_data.get('publishers') ,  #  this field choicen from publishers list
    #                 tags        = validated_data.get('tags'),    #  this field choicen from tags list 
    #                 authors     = validated_data.get('authors'),   # this field choicen from likes list 
    #                 # author      = self.context.get('request').user, # username  get from username list  
    #     )
    #     book = super().create(validated_data)
    #     return book
                    

    # def create(self, validated_data):
    #     publishers_data = validated_data.pop('publishers')
    #     authors_data = validated_data.pop('authors')
    #     tags_data = validated_data.pop('tags')
        
    #     book = Book.objects.create(**validated_data)
        
    #     for publisher_data in publishers_data:
    #         Book.objects.create(book=book, **publisher_data)
        
    #     for author_data in authors_data:
    #         Book.objects.create(book=book, **author_data)
        
    #     for tag_data in tags_data:
    #         Book.objects.create(book=book, **tag_data)
    #     return book