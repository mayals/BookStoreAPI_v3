from django.contrib import admin
from .models import Category, Publisher, Author, Tag, Review, Book
    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display  = ['id', 'name','created_at']
    list_filter   = ['name']
    search_fields = ['name']

@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display  =  ['id', 'name', 'created_at', 'updated_at']
    list_filter   =  ['name']
    search_fields = ("name",)
      
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display  = ('id',"first_name", "last_name", 'created_at', 'updated_at')
    list_filter   = ("first_name", "last_name", 'created_at', 'updated_at',)
    search_fields = ("first_name", "last_name")

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display  = ['id', 'name']
    list_filter   = ['name']
    search_fields = ['name']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'book', 'user', 'integerRating', 'textRating', 'created_at', 'updated_at']
    list_filter  = [ 'book', 'user', 'integerRating', 'created_at', 'updated_at']
    search_fields = ['book', 'user']
   


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display  = ['id', 'ISBN', 'title', 'category', 'average_rating', 'publish_date',
                    'num_pages', 'condition', 'stock', 'created_at', 'updated_at']                   

    list_filter   = ['title', 'category', 'publishers', 'authors']              
    search_fields = ['title', 'authors']
    
    