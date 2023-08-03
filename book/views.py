from django.shortcuts import get_object_or_404
from rest_framework import viewsets,mixins,permissions, generics
from .models import Category,Publisher,Author,Tag,Review,Book
from .serializers import CategorySerializer,PublisherSerializer,AuthorSerializer,TagSerializer,ReviewSerializer,BookSerializer
from rest_framework.response import Response
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


    # Important NOTE we must write create function because we must add the the data that insert in the fields:
    # of types ForeignKey field and ManyToManyField  :
    # 'category' , 'publishers' , 'authors' and 'tags'
    # without this create function inside BookViewSet these fields remain empty ! 
    def create(self,request,*args, **kwargs):
        data = request.data
        print(data)  
        title = data.get('title')
        if title :
            new_book = Book.objects.create( title= data.get('title')) # this for create book with only title field
            new_book.save()
            print('new_book='+ str(new_book))
 
            category = data.get('category')
            if category :
                # adding  the content of category field content
                cat_name = data.get('category',[])
                print('cat_name='+ str(type(cat_name)))   # string 
                print('cat_name='+ str(cat_name))
                if cat_name: #string
                    category_obj = Category.objects.get(name= cat_name) # get object from its name
                    print('category_obj='+ str(category_obj))
                    new_book.category = category_obj 
                    new_book.save()
                    print('new_book.category='+ str(new_book.category))
        
                    publishers = data.get('publishers')
                    if publishers :
                        # adding the content of publishers field
                        publishers_names = request.data.get('publishers',[])
                        print('publishers_names='+ str(publishers_names))    
                        print('publishers_names='+ str(type(publishers_names)))    # string       
                        if publishers_names : #string
                            publishers_names_list=publishers_names.split(',')      # list of names
                            for item in publishers_names_list: # loop on list to took the names
                                print('item='+ str(item))   
                                try:
                                    publisher_obj, created = Publisher.objects.get_or_create(name=item) # get object by its name
                                    print('publisher_obj='+ str(publisher_obj))
                                    new_book.publishers.add(publisher_obj) #add object
                                    new_book.save()
                                except Publisher.DoesNotExist:
                                    pass 
        

                                authors = data.get('authors')
                                if authors : 
                                    # adding the content of authors field
                                    authors_full_names = request.data.get('authors',[])
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

                                            
                                            tags = data.get('tags')
                                            if tags :
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
                                                        return Response(serializer.data, status=status.HTTP_201_CREATED)
 
        return Response({"error": "the fields : ('title' - 'category' - 'publishers' - 'authors' - 'tags') are required"})

   
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


