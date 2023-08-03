from django.shortcuts import get_object_or_404
from rest_framework import viewsets,mixins,permissions, generics
from .models import Category,Publisher,Author,Tag,Review,Book
from .serializers import CategorySerializer,PublisherSerializer,AuthorSerializer,TagSerializer,ReviewSerializer,BookSerializer
from rest_framework.response import Response

#https://www.django-rest-framework.org/api-guide/viewsets/#custom-viewset-base-classes
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
            self.permission_classes = [permissions.AllowAny]       
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
            self.permission_classes = [permissions.AllowAny]       
        return super().get_permissions()    



class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'slug' 


# class BookListCreateAPIView(generics.ListCreateAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer



class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    # def get_queryset(self):
    #     books = Book.objects.all()
    #     return books
    
    def create(self,request,*args, **kwargs):
        data = request.data
        print(data)
        new_book = Book.objects.create(
                                title      = data.get('title') ,  # any title , must be unique
                                # category   = data.get('category') , # this field choicen from categories list 
        )
        new_book.save()
        print('new_book='+ str(new_book))

        # adding  the content of category field content
        cat_name = data.get('category')
        print('cat_name='+ str(type(cat_name)))   # string 
        print('cat_name='+ str(cat_name))
        if cat_name:
            category_obj = Category.objects.get(name= cat_name)
            print('category_obj='+ str(category_obj))
            new_book.category = category_obj 
            new_book.save()
            print('new_book.category='+ str(new_book.category))

        # adding the content of publishers field
        publishers_names = request.data.get('publishers')
        print('publishers_names='+ str(publishers_names))    
        print('publishers_names='+ str(type(publishers_names)))     # string       
        if publishers_names :
            publishers_names_list=publishers_names.split(',')
            for item in publishers_names_list:
                print('item='+ str(item))   
                try:
                    publisher_obj, created = Publisher.objects.get_or_create(name=item)
                    print('publisher_obj='+ str(publisher_obj))
                    new_book.publishers.add(publisher_obj)
                    new_book.save()
                except Publisher.DoesNotExist:
                    pass    
        
        
        # adding the content of authors field
        authors_full_names = request.data.get('authors')
        print('authors_full_names='+ str(authors_full_names))    
        print('authors_full_names='+ str(type(authors_full_names)))     # string       
        if authors_full_names:
            authors_full_names_list=authors_full_names.split(',')
            for item in authors_full_names_list:
                print('item='+ str(item))   
                try:
                    author_obj, created = Author.objects.get_or_create(full_name=item)
                    print('author_obj='+ str(author_obj))
                    new_book.authors.add(author_obj)
                    new_book.save()
                except Author.DoesNotExist:
                    pass   


        
        # adding the content of tags field
        tags_names = request.data.get('tags')
        print('tags_names='+ str(tags_names))    
        print('tags_names='+ str(type(tags_names)))     # string       
        if tags_names:
            tags_names_list=tags_names.split(',')
            for item in tags_names_list:
                print('item='+ str(item))   
                try:
                    tag_obj, created = Tag.objects.get_or_create(name=item)
                    print('tag_obj='+ str(tag_obj))
                    new_book.tags.add(tag_obj)
                    new_book.save()
                except Author.DoesNotExist:
                    pass   


        serializer = BookSerializer(new_book)
        return Response(serializer.data)







class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
       
    # def perform_create(self, serializer): 
    #     user = self.request.user 
    #     book = self.kwargs.get('course_pk')
    #     serializer.save(user=user,book=book) 


