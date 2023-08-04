from django.shortcuts import get_object_or_404
from rest_framework import viewsets,mixins,permissions, generics
from .models import Category,Publisher,Author,Tag,Review,Book
from .serializers import CategorySerializer,PublisherSerializer,AuthorSerializer,TagSerializer,ReviewSerializer,BookSerializer
from rest_framework import response
from rest_framework import status
#https://www.django-rest-framework.org/api-guide/viewsets/#custom-viewset-base-classes


# Not: category have no permission for update
class CategoryViewSet(viewsets.mixins.CreateModelMixin, mixins.ListModelMixin, 
                      mixins.RetrieveModelMixin,mixins.DestroyModelMixin, viewsets.GenericViewSet):                      
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'slug' 

    def get_permissions(self):
        if self.action in["create","destroy"]:
            self.permission_classes = [permissions.IsAuthenticated,permissions.IsAdminUser]   
        else:
            self.permission_classes = [permissions.IsAuthenticated]       
        return super().get_permissions()



class PublisherViewSet(viewsets.ModelViewSet):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'slug' 

    def get_permissions(self):
        if self.action in["create","destroy"]:
            self.permission_classes = [permissions.IsAuthenticated,permissions.IsAdminUser]   
        else:
            self.permission_classes = [permissions.IsAuthenticated]       
        return super().get_permissions()




class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'slug'

    def get_permissions(self):
        if self.action in ['create','update','partial_update','destroy']:
            self.permission_classes = [permissions.IsAuthenticated,permissions.IsAdminUser]   
        else:
            self.permission_classes = [permissions.IsAuthenticated]       
        return super().get_permissions()    



class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'slug' 

    def get_permissions(self):
        if self.action in ['create','update','partial_update','destroy']:
            self.permission_classes = [permissions.IsAuthenticated,permissions.IsAdminUser]   
        else:
            self.permission_classes = [permissions.IsAuthenticated]       
        return super().get_permissions()

 


# https://docs.djangoproject.com/en/4.2/topics/db/models/#extra-fields-on-many-to-many-relationships
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'slug' 
    
    def get_permissions(self):
        if self.action in ['create','update','partial_update','destroy']:
            self.permission_classes = [permissions.IsAuthenticated,permissions.IsAdminUser]   
        else:
            self.permission_classes = [permissions.IsAuthenticated]       
        return super().get_permissions()

    def get_serializer_class(self):
          self.serializer_class = BookSerializer 
          return super().get_serializer_class()
    

    # Important NOTE we must write create function because we must add the the data that insert in the fields:
    # of types ForeignKey field and ManyToManyField  :
    # 'category' , 'publishers' , 'authors' and 'tags'
    # without this create function inside BookViewSet these fields remain empty ! 
    def create(self,request,*args, **kwargs):
        data = request.data
        # print(data) 
        print(data['title'])
        if data['title'] == "" or data['category']  == "" or data['publishers']  == "" or data['authors']  == "" or data['tags'] == "" :
            print(data['title'])
            return response.Response({"error": "the fields : ( title - category - publishers - authors - tags ) are required"})
    
        title = data.get('title')
        if  Book.objects.filter(title=title).exists():
            return response.Response({"error":"The book's title must be unique"})
        
        # this for create book with only title field
        new_book = Book.objects.create(title= data.get('title'))
        new_book.save()
        print('new_book='+ str(new_book))
    
         # adding  the content of category field content
        category = data.get('category')
        cat_name = data.get('category',[])        #string
        print('cat_name='+ str(type(cat_name)))   # string 
        print('cat_name='+ str(cat_name))
        category_obj = Category.objects.get(name= cat_name) #obj # get category object from its name
        print('category_obj='+ str(category_obj))
        new_book.category = category_obj 
        new_book.save()
        print('new_book.category='+ str(new_book.category))

        # adding the content of publishers field
        publishers = data.get('publishers')    
        publishers_names = request.data.get('publishers',[])
        print('publishers_names='+ str(publishers_names))    
        print('publishers_names='+ str(type(publishers_names)))    # list of name strings      
        if publishers_names : # list of publishers names strings ['strnamepub1','strnamepub2','',...]
            for item in publishers_names: # loop on list to took the names
                print('item='+ str(item))           
                publisher_obj, created = Publisher.objects.get_or_create(name=item) # get object by its name
                new_book.publishers.add(publisher_obj) #add object 
        new_book.save()
                    
        # adding the content of authors field
        authors = data.get('authors')        
        authors_full_names = request.data.get('authors',[])
        print('authors_full_names='+ str(authors_full_names))    
        print('authors_full_names='+ str(type(authors_full_names)))     # string       
        if authors_full_names:
            for item in authors_full_names:
                print('item='+ str(item))   
                author_obj, created = Author.objects.get_or_create(full_name=item)
                # print('author_obj='+ str(author_obj))
                new_book.authors.add(author_obj)
        new_book.save()
                                
        # adding the content of tags field                        
        tags = data.get('tags')
        tags_names = request.data.get('tags')
        print('tags_names='+ str(tags_names))    
        print('tags_names='+ str(type(tags_names)))     # string       
        if tags_names:
            for item in tags_names:
                print('item='+ str(item))   
                tag_obj, created = Tag.objects.get_or_create(name=item)
                # print('tag_obj='+ str(tag_obj))
                new_book.tags.add(tag_obj)
        new_book.save()
        
        serializer = BookSerializer(new_book)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)
# else:        
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

       

   
# class BookListCreateAPIView(generics.ListCreateAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer




class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
       
    # def perform_create(self, serializer): 
    #     user = self.request.user 
    #     book = self.kwargs.get('course_pk')
    #     serializer.save(user=user,book=book) 


