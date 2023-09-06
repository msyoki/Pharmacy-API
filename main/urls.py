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
from pharmacy.views import register_user,UserUpdateView,ProductViewSet,SaleViewSet,CategoryViewSet,SubCategoryViewSet,SupplierViewSet,UserViewSet, CustomTokenObtainPairView

router = DefaultRouter()

router.register(r'suppliers',SupplierViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'subcategories', SubCategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'sales', SaleViewSet)
router.register(r'users', UserViewSet)



urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include(router.urls)),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Add this line
    path('api/user/update/', UserUpdateView.as_view(), name='user-update'),
    path('api/register/', register_user, name='register_user'),
]
