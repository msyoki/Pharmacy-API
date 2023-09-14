"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from pharmacy.views import StockViewSet,register_user,calculate_total_sales,calculate_daily_sales_total,calculate_total_non_credit_sales,calculate_credit_sales_balance,UserUpdateView,ProductViewSet,SaleViewSet,SupplierViewSet,UserViewSet, CustomTokenObtainPairView

router = DefaultRouter()

router.register(r'suppliers',SupplierViewSet)
router.register(r'products', ProductViewSet)
router.register(r'sales', SaleViewSet) 
router.register(r'stock', StockViewSet) 
router.register(r'users', UserViewSet)




urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include(router.urls)),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Add this line
    path('api/user/update/', UserUpdateView.as_view(), name='user-update'),
    path('api/register/', register_user, name='register_user'),
    path('api/report/',calculate_daily_sales_total, name='sale_report'),
    path('api/allsales/',calculate_total_sales, name='sales_totals'),
    path('api/cash/',calculate_total_non_credit_sales, name='cash_sales_totals'),
    path('api/credit/',calculate_credit_sales_balance, name='cash_credit_totals')     
]
calculate_total_sales