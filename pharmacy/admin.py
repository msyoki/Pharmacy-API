from django.contrib import admin
from .models import Product, Sale,Supplier, Category,SubCategory

# Register your models here.

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'total_amount','is_credit_sale')


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_person', 'contact_email', 'contact_phone')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'quantity', 'price','category','subcategory')
 
@admin.register(Category)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name')

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'category')
   