from django.urls import path,include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import  TokenObtainPairView,  TokenRefreshView
from user import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register('users', views.UserViewSet,basename="users")               # UserModel   {'get': 'list'}-{'get': 'retrieve'}-{'delete': 'destroy'}
router.register('profiles', views.UserViewSet,basename="profiles")         # UserProfile
router.register('sms-codes', views.SMSCodeViewSet,basename="sms-codes")    # SMSCode


# The API URLs are now determined automatically by the router.
urlpatterns =  router.urls  + [
    
    # UserModel  model
    path('register/', views.UserViewSet.as_view({'post': 'create'}), name='register'),    # UserModel {'post': 'create'}
    #User ConfirmEmail
    path('confirm-email/<uidb64>/<str:token>/',views.ConfirmEmailView.as_view(), name='confirm-email'),
    #User JWT Authentication
    path('login/get-token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),
    #User password
    path("reset-password/", include("django_rest_passwordreset.urls", namespace="password_reset")),
    
    
    # UserProfile model 




    # SMSCode model
    # path('smscode/', views.SMSCodeViewSet.as_view(), name='sms_code'),
]


