from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import smart_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import status, viewsets,  permissions, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from.models import UserProfile, SMSCode
from .serializers import UserRegistrationSerializer, UserModelSerializer,ConfirmEmailSerializer, UserProfileSerializer, SMSCodeSerializer 
# https://github.com/GeeWee/django-auto-prefetching
import django_auto_prefetching





class UserViewSet(django_auto_prefetching.AutoPrefetchViewSetMixin, viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserModelSerializer
    permission_classes = [permissions.IsAuthenticated]
    # pagination_class = CustomPagination

    # Define a get_queryset method that returns only active users for non-superusers
    def get_queryset(self):
        if self.request.user.is_superuser:
            return super().get_queryset()
        raise PermissionDenied("You do not have permission to access the list of users.")

    # Define a get_serializer_class method that uses a different serializer for user creation
    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegistrationSerializer
        return super().get_serializer_class()

    # Define a get_permissions method that sets custom permissions based on the action    
    def get_permissions(self):
        if self.action == 'destroy':
            return {permissions.IsAuthenticated(), permissions.IsAdminUser()}
        if self.action == 'create':
            return {permissions.AllowAny()}
        return super().get_permissions()




class ConfirmEmailView(APIView):
    queryset = get_user_model().objects.all()
    serializer_class = ConfirmEmailSerializer
    permission_classes = []

    def get(self, request, uidb64, token):
        try:
            uid = smart_str(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            return Response({"error": "Invalid user ID"}, status=400)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.is_verifiedEmail = True
            user.save()
            return Response({"message": "Email confirmation successful"})
        else:
            return Response({"error": "Invalid token"}, status=400)
    

#######################################################################################################################################
class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()



    
class SMSCodeViewSet(viewsets.ModelViewSet):
    serializer_class = SMSCodeSerializer 
    queryset = SMSCode.objects.all()


