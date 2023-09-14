from django.contrib import admin
from .models import CustomUser,Product,SaleItem, Sale,Supplier,StockAlert,Stock

# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id','email', 'first_name','last_name', 'is_staff','is_admin','is_superuser')

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id','created','user')

@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity','sale')

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity','receivedby','captured')



@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_person', 'contact_email', 'contact_phone')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'price')


@admin.register(StockAlert)
class StockAlertAdmin(admin.ModelAdmin):
    list_display = ('product','threshold','is_active')


# @admin.register(Category)
# class SubCategoryAdmin(admin.ModelAdmin):
#     list_display = ('id','name')

# @admin.register(SubCategory)
# class SubCategoryAdmin(admin.ModelAdmin):
#     list_display = ('id','name', 'category')
   