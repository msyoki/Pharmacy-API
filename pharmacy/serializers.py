from rest_framework import serializers
from .models import Product, CreditSale,CashSale,Supplier,Category,SubCategory


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

class CreditSaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditSale
        fields = '__all__'

class CashSaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashSale
        fields = '__all__'

