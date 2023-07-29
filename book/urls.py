from django.urls import path
from rest_framework.routers import DefaultRouter
from book import views



# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register('categories', views.CategoryViewSet, basename="categories")     # Category  
router.register('publishers', views.PublisherViewSet, basename="publishers")    # Publisher 
router.register('authors', views.AuthorViewSet, basename="authors")             # Author
router.register('tags', views.TagViewSet, basename="tags")                      # Tags
router.register('reviewinfos', views.ReviewInfoViewSet, basename="reviewinfos")     # ReviewInfo
router.register('books', views.BookViewSet, basename="books")                   # Book


# The API URLs are now determined automatically by the router.
urlpatterns =  router.urls  + [
    path('books/categories/<str:slug>/', views.BookViewSet.as_view({'get': 'retrieve'}, name='book:categories-detail')), #name=basename-detail
    path('books/publishers/<str:slug>/', views.BookViewSet.as_view({'get': 'retrieve'}, name='book:publishers-detail')),  #name=basename-detail
    path('books/authors/<str:slug>/', views.BookViewSet.as_view({'get': 'retrieve'}, name='book:authors-detail')),  #name=basename-detail
    path('books/tags/<str:slug>/', views.TagViewSet.as_view({'get': 'retrieve'}, name='book:authors-detail')),  #name=basename-detail

    
    # UserModel  model
    # path('register/', views.UserViewSet.as_view({'post': 'create'}), name='register'),    # UserModel
 
]


