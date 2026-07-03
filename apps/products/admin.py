from django.contrib import admin
from .models import Category, Product, PhotoProduct

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)
    search_fields = ('name',)
    list_filter = ('parent',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'category', 'status', 'price', 'quantity')
    prepopulated_fields = {'slug':('name',)}
    ordering = ('name',)
    search_fields = ('name', 'description')
    list_filter = ('category', 'status', 'price')
    list_editable = ('price',)

@admin.register(PhotoProduct)
class PhotoProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'image', 'is_main')
    search_fields = ('product__name',)
    list_filter = ('is_main',)
    ordering = ('product',)