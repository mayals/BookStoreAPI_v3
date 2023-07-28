from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers
from.models import UserModel, UserProfile, SMSCode
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


# ---[POST]---------- this serializer used only for registeration  [POST]---------------------------#
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type':'password'})
    # Meta class to specify the model and its fields to be serialized
    class Meta:
        model = UserModel
        fields = ['id','email','first_name','last_name','password'] 
        extra_kwargs = {'email': {'required': True},
                        'first_name': {'required': True},
                        'last_name': {'required': True},
        }
    # Method to validate the email entered by the user
    def validate_email(self, value):
        if UserModel.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email address already exists.")
        return value 
    # Method to validate the password entered by the user
    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value
    
    # Create a new user object using the validated data
    def create(self, validated_data):
        user = UserModel.objects.create_user(
                                    email = validated_data['email'],
                                    first_name=validated_data['first_name'],
                                    last_name=validated_data['last_name'],
                                    password=validated_data['password'],
                                    is_verifiedEmail=False
        )
        return user
    


class ConfirmEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['id', 'email', 'first_name', 'last_name', 'is_verifiedEmail', 'enable_two_factor_authentication', 'created_at']





class CustomTokenObtainPairSerializer(TokenObtainPairSerializer): 
    """Override default token login to include user data"""

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        if not user.is_verifiedEmail:
            raise serializers.ValidationError({"error":"Email is not verified."})
        data.update(
            {
                "id": self.user.id,
                "email": self.user.email,
                "first_name": self.user.first_name,
                "last_name": self.user.last_name,
                "is_superuser": self.user.is_superuser,
                "is_staff": self.user.is_staff,
                "is_verifiedEmail": self.user.is_verifiedEmail
            }
        )
        return data
    






class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['id', 'email', 'first_name', 'last_name', 'is_verifiedEmail', 'enable_two_factor_authentication', 'created_at']






class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'bio', 'profile_image', 'date_of_birth', 'gender', 'address', 'phone_number', 'created_at', 'updated_at']




class SMSCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMSCode
        fields = ['id', 'user', 'OTP_code', 'created_at']