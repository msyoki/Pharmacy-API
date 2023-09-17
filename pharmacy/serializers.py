from rest_framework import serializers
from .models import Product,SaleItem,Sale,Supplier,Stock,Patient,LabRequest,PatientNotes
from django.contrib.auth import get_user_model
# api/serializers.py
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.humanize.templatetags.humanize import naturaltime


CustomUser = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims to the token payload
        token['username'] = user.username
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['is_active'] = user.is_active
        token['is_admin'] = user.is_admin

        return token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id','username','email','first_name','last_name','is_active', 'is_admin','is_staff')
    
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
        

class LabRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabRequest
        fields = '__all__'

class PatientNotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientNotes
        fields = '__all__'

class SaleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleItem
        fields = ('product', 'quantity')

class SaleSerializer(serializers.ModelSerializer):
    sale_items = SaleItemSerializer(many=True, read_only=True)

    class Meta:
        model = Sale
        fields = '__all__'

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'
