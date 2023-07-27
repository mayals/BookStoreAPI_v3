from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import  TokenObtainPairView,  TokenRefreshView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('user.urls')),
    # path('books/', include('book.urls')),
    # path('ecommerces/', include('ecommerce.urls')),
    
    # path('api-auth/', include('rest_framework.urls')), not need 

   




]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)