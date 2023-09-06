
from rest_framework import viewsets,status,permissions
from rest_framework.decorators import api_view,authentication_classes, permission_classes
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from .models import Product,Supplier, Sale,Category,SubCategory,StockAlert
from .serializers import ProductSerializer,CategorySerializer,SubCategorySerializer,SupplierSerializer, SaleSerializer,UserSerializer,CustomTokenObtainPairSerializer,UserUpdateSerializer

CustomUser = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ['get']

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer  # Use the custom serializer


@api_view(['POST'])
@authentication_classes([])  # Disable authentication for this view
@permission_classes([])  # Disable permission checks for this view
def register_user(request):
    password = request.data.get('password')
    email = request.data.get('email')
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    is_admin = request.data.get('is_admin', False)

    if not password or not email:
        return Response({'error': 'Please provide email and password.'}, status=status.HTTP_400_BAD_REQUEST)

    user, created = CustomUser.objects.get_or_create(email=email,first_name=first_name,last_name=last_name)
    if created:
        user.set_password(password)
        user.is_admin = is_admin  # Set the is_admin field
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response({'error': 'Username or email already exists.'}, status=status.HTTP_400_BAD_REQUEST)


class UserUpdateView(UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Get the user making the request
        return self.request.user

    def update(self, request, *args, **kwargs):
        # Allow partial updates (including password)
        instance = self.get_object()
        partial = kwargs.pop('partial', True)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [permissions.AllowAny]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    permission_classes = [permissions.AllowAny]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        product_name = request.data.get('name')

        if Product.objects.filter(name=product_name).exists():
            return Response(
                {"error": "A product with this name already exists."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Get the original quantity before updating
        original_quantity = instance.quantity

        self.perform_update(serializer)

        # Get the updated quantity after updating
        updated_quantity = serializer.validated_data.get('quantity')

        # Get the stockalert instance
        stock_alert= StockAlert.objects.get(product=instance)

        # Check if the quantity has changed and take action if needed
        if updated_quantity > stock_alert.threshold:
            # Perform your actions here, e.g., trigger alerts, update stock, etc.
            stock_alert.is_active = False
            stock_alert.save()

           
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)


class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
