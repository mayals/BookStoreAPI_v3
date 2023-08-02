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
        
        cat_name = data.get('category')
        
        print('cat_name='+ str(cat_name))
        if cat_name:
            category_obj = Category.objects.get(name= cat_name)
            print('category_obj='+ str(category_obj))
            new_book.category = category_obj 
            new_book.save()
            print('new_book='+ str(new_book))
             
                         
        for publisher_data in data.get('publishers_data',[]):
            try:
                publisher_obj = Publisher.objects.get(name= publisher_data.get('name'))
                print('publisher_obj='+ str(publisher_obj))
                new_book.publishers.add(publisher_obj)
                new_book.save()
                print('new_book='+ str(new_book))
            except Publisher.DoesNotExist:
                pass    
        for author_data in data.get('authors_data',[]):
            try:
                author_obj = Author.objects.get(full_name= author_data.get('full_name'))
                new_book.authors.add(author_obj)    
                new_book.save()
            except Author.DoesNotExist:
                pass
        for tag_data in data.get('tags_data',[]):
            try:
                tag_obj = Tag.objects.get(name= tag_data.get('name'))
                new_book.tags.add(tag_obj)
                new_book.save()
            except Tag.DoesNotExist:
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


