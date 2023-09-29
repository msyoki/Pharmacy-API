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
from pharmacy.views import calculate_credit_sales_balance_lab_today,calculate_credit_sales_balance_today,credit_sales_summary_lab,cash_sales_summary_lab,StockViewSet,LabRequestViewSet,calculate_total_non_credit_sales_lab,calculate_total_sale_lab,calculate_credit_sales_balance_lab,get_patient_notes,PatientNotesViewSet,sale_summary,stock_alerts,PatientViewSet,cash_sales_summary,credit_sales_summary,all_captured_stock,register_user,calculate_total_sales,calculate_daily_sales_total,calculate_total_non_credit_sales,calculate_credit_sales_balance,UserUpdateView,ProductViewSet,SaleViewSet,SupplierViewSet,UserViewSet, CustomTokenObtainPairView

router = DefaultRouter()

router.register(r'suppliers',SupplierViewSet)
router.register(r'products', ProductViewSet)
router.register(r'sales', SaleViewSet) 
router.register(r'stock', StockViewSet) 
router.register(r'users', UserViewSet)
router.register(r'patients',PatientViewSet)
router.register(r'patientnotes',PatientNotesViewSet)
router.register(r'labrequest',LabRequestViewSet)




urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include(router.urls)),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Add this line
    path('api/user/update/', UserUpdateView.as_view(), name='user-update'),
    path('api/register/', register_user, name='register_user'),
    path('api/report/',calculate_daily_sales_total, name='sale_report'),
    path('api/allsales/',calculate_total_sales, name='sales_totals'),
    path('api/allsaleslab/',calculate_total_sale_lab, name='sales_totals_lab'),
    path('api/cash/',calculate_total_non_credit_sales, name='cash_sales_totals'),
    path('api/credit/',calculate_credit_sales_balance, name='cash_credit_totals'),
    path('api/credit/today/',calculate_credit_sales_balance_today, name='calculate_credit_sales_balance_today'),
    
    path('api/cashlab/',calculate_total_non_credit_sales_lab, name='cash_sales_totals_lab'),
    path('api/creditlab/',calculate_credit_sales_balance_lab, name='cash_credit_totals_lab'),
    path('api/creditlab/today/',calculate_credit_sales_balance_lab_today, name='calculate_credit_sales_balance_today'),
    
    path('api/allstock/',all_captured_stock, name='all_captured_stock'),
    path('api/cssummary/',credit_sales_summary, name='credit_sales_summary'),  
    path('api/cassummary/',cash_sales_summary, name='cash_sales_summary'),
    path('api/cssummarylab/',credit_sales_summary_lab, name='credit_sales_summary_lab'),  
    path('api/cassummarylab/',cash_sales_summary_lab, name='cash_sales_summary_lab'),
    path('api/salesummary/<int:pk>/',sale_summary, name='sale_summary'),
    path('api/stockalerts/',stock_alerts, name='stock_alerts'),
    path('api/getpatientnotes/<int:pk>/',get_patient_notes, name='get_patient_notes')

]
