from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('user.urls')),  # user application url
    path('books/', include('book.urls')),  # book application url
    # path('ecommerces/', include('ecommerce.urls')),
    
    # path('api-auth/', include('rest_framework.urls')), not need 

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)