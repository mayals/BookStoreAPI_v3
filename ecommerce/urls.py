from django.urls import path
from rest_framework.routers import DefaultRouter
from ecommerce import views



# Create a router and register our viewsets with it.
router = DefaultRouter()
#router.register('orders', views.OrderViewSet, basename="orders")     # Order  




# The API URLs are now determined automatically by the router.
urlpatterns =  router.urls  + [
    # Order Endpoints:
    #path('orders/orders/<str:order_id>/', views.OrderViewSet.as_view({'get':'retrieve'}, name='ecommerce:orders-detail')),   #name=basename-detail
    path('orders/orders/create_order/', views.OrderCreateAPIView.as_view(), name="create_order"),
    #('orders/<str:book_id>/create_order/', views.OrderCreateAPIView.as_view(), name="create_order"),
    # path('ordrs/orders/<int:id>/cancel/', views.ReviewRetrieveUpdateDestroyAPIView.as_view(),name='retrieve-update-destroy-review'),
    # Cart and Checkout Endpoints:
    # /cart/add
    # /cart
    # /cart/update/{cart_item_id}
    # /cart/remove/{cart_item_id}
    # /checkout
    
]


