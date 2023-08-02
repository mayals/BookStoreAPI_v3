from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
# https://pypi.org/project/shortuuid/
from shortuuid.django_fields import ShortUUIDField 




class Category(models.Model):
    id          = ShortUUIDField(primary_key=True, unique=True, length=6, max_length=6, editable=False)
    name        = models.CharField(max_length=100, unique=True, null=True, blank=False) 
    slug        = models.SlugField(max_length=120, blank=True, null=True)
    icon        = models.ImageField(upload_to = "book/category/%Y/%m/%d/", blank=True, null=True)
    created_at  = models.DateTimeField(auto_now_add=True,auto_now=False)
       
    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs): 
            self.slug = slugify(self.name)
            super().save(*args, **kwargs)  # Call the "real" save() method.       
    
    def get_absolute_url(self):
        return reverse('category-detail', kwargs = {'slug':self.slug})      # view_name='{model_name}-detail'    
    
    
    class Meta:
        ordering = ('name',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'




class Publisher(models.Model):
    id            = ShortUUIDField(primary_key=True, unique=True, length=6, max_length=6, editable=False)
    name           = models.CharField(max_length=30, null=True)
    slug           = models.SlugField(max_length=120, blank=True, null=True)
    address        = models.CharField(max_length=50, null=True, blank=True)
    website        = models.URLField(max_length = 255, null=True, blank=True)
    social_twitter = models.URLField(max_length = 255, null=True, blank=True)
    created_at     = models.DateTimeField(auto_now_add=True,auto_now=False, null=True)
    updated_at     = models.DateTimeField(auto_now_add=False,auto_now=True, null=True)
    # city           = models.CharField(max_length=60, null=True)
    # state_province = models.CharField(max_length=30, null=True)
    # country        = models.CharField(max_length=50, null=True)
   
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs): 
            self.slug = slugify(self.name)
            super().save(*args, **kwargs)  #                                 # Call the "real" save() method.   

    def get_absolute_url(self):
        return reverse('publisher_detail', kwargs = {'slug':self.slug})   # view_name='{model_name}-detail'
    
    class Meta:
        ordering = ('name',)
        verbose_name = 'Publisher'
        verbose_name_plural = 'Publishers'





class Author(models.Model):
    id         = ShortUUIDField(primary_key=True, unique=True, length=6, max_length=6, editable=False)
    first_name = models.CharField(max_length=10, null=True)
    last_name  = models.CharField(max_length=10, null=True)
    slug       = models.SlugField(max_length=120, blank=True, null=True)
    email      = models.EmailField(null=True, blank=True)
    bio        = models.TextField(blank=True)
    pic        = models.ImageField(upload_to = "book/author/%Y/%m/%d/",blank=True)
    website    = models.URLField(max_length = 255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False,auto_now=True, null=True)
    
    @property
    def get_author_fullname(self):
        return f'{self.first_name} {self.last_name}'
    
    def __str__(self):
        return self.get_author_fullname

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.first_name) +' '+ str(self.last_name))
        super().save(*args, **kwargs)      # Call the "real" save() method. 
    
    #vue view_name='{model_name}-detail'
    def get_absolute_url(self):
        return reverse('author-detail', kwargs = {'slug':self.slug})  
    
    class Meta:
        ordering = ('first_name',)
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'
        unique_together = ['first_name','last_name']
     

       


class Tag(models.Model):
    # Represents a tag for a book
    id   = ShortUUIDField(primary_key=True, unique=True, length=6, max_length=6, editable=False)
    name = models.CharField(max_length=255,blank=False)
    slug = models.SlugField(max_length=120, blank=True, null=True)
     
    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.name))
        super().save(*args, **kwargs)           # Call the "real" save() method. 
    
    def __str__(self):
        return self.slug



# Review is the table that contain users reviews 
class Review(models.Model):
    id             = ShortUUIDField(primary_key=True, unique=True, length=6, max_length=6, editable=False)
    user           = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True , blank=False, related_name = 'reviews')
    book           = models.ForeignKey('book.Book', on_delete=models.CASCADE, null=True , blank=False ,related_name = 'reviews')
    created_at     = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at     = models.DateTimeField(auto_now_add=False, auto_now=True)
    
    rating_value   = models.PositiveIntegerField(default=0, validators= [ MinValueValidator(0), MaxValueValidator(5)])
    rating_text    = models.TextField(blank=True, null=True)
     
    def __str__(self):
        return f"Rating of '( {self.rating_value} ) stars' by {self.user.get_user_fullname}"




class Book(models.Model):
    new = 'New'
    old = 'Old'
    CONDITION_CHOICES = [
                    (new,'New'),
                    (old,'Old'),
    ]
    T = 'In Stock'
    F = 'Out Of Stock'
    STOCK_CHOICES = [
                    (T,'In Stock'),
                    (F,'Out Of Stock'),
    ]       
    id               = ShortUUIDField(primary_key=True, unique=True, length=6, max_length=6, editable=False)
    ISBN             = models.CharField(max_length=13, unique=True, blank=True, null=True)
    title            = models.CharField(max_length=100, unique=True, blank=False, null=True)
    slug             = models.SlugField(max_length=120, blank=True, null=True)
    category         = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=False, related_name='books_category')            
    publishers       = models.ManyToManyField(Publisher, blank=False)
    authors          = models.ManyToManyField(Author, blank=False) 
    tags             = models.ManyToManyField(Tag, blank=False)
    num_pages        = models.IntegerField(blank=True, null=True)
    cover_image      = models.FileField(upload_to = "book/cover_image/%Y/%m/%d/", blank=True)
    page_image       = models.FileField(upload_to = "book/page_image/%Y/%m/%d/", blank=True)
    condition        = models.CharField(max_length=20, choices= CONDITION_CHOICES, null=True, blank=True)
    stock            = models.CharField(max_length=20, choices= STOCK_CHOICES, null=True, blank=True)
    created_at       = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at       = models.DateTimeField(auto_now_add=False, auto_now=True)
    publish_date     = models.DateField(null=True, blank=True)
    
    book_reviews     = models.PositiveIntegerField(default=0, validators= [ MinValueValidator(0), MaxValueValidator(5)], blank=True)                                     
    reviews_count    = models.IntegerField(default=0)
    average_rating   = models.FloatField(default=0.0)
    
    
    
     
    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):                 # Call the "real" save() method.
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)                                 
    
    # def calculate_average_rating(self):
    #     book_reviews = self.reviews_count.all()
    #     if book_reviews:
    #         total_ratings = sum(rev.rating_value for rev in book_reviews)
    #         return total_ratings / len(book_reviews)
    #     return 0.0
    
    def get_absolute_url(self):
        return reverse('book-detail', kwargs = {'slug':self.slug})   # view_name='{model_name}-detail'
    
    class Meta:
        indexes = [
            models.Index(fields=['id']),
            models.Index(fields=['created_at']),
        ]
        ordering = ('title',)
        verbose_name = 'Book'
        verbose_name_plural = 'Books'




