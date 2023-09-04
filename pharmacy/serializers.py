from rest_framework import serializers
from .models import Product,Sale,Supplier,Category,SubCategory
from django.contrib.auth import get_user_model
# api/serializers.py
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

CustomUser = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims to the token payload
        token['email'] = user.email
        token['first_name'] = user.username
        token['last_name'] = user.username
        token['is_active'] = user.is_active
        token['is_admin'] = user.is_admin

        return token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email','first_name','last_name', 'password', 'is_active', 'is_admin','is_staff')
        extra_kwargs = {'password': {'write_only': True}}  # Hide password field in response

class UserUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)  # Include password field

    class Meta:
        model = CustomUser
        fields = ('first_name','last_name','password')  # Add fields to be updated


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'

class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = '__all__'


