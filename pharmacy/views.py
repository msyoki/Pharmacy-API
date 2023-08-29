from rest_framework import viewsets
from .models import Product,Supplier, CreditSale,CashSale
from .serializers import ProductSerializer,SupplierSerializer, CreditSaleSerializer, CashSaleSerializer


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CreditSaleViewSet(viewsets.ModelViewSet):
    queryset = CreditSale.objects.all()
    serializer_class = CreditSaleSerializer

class CashSaleViewSet(viewsets.ModelViewSet):
    queryset = CashSale.objects.all()
    serializer_class = CashSaleSerializer
