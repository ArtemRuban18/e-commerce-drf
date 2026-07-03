from .models import Category, Product
from django.shortcuts import get_object_or_404

class CategoryService:
    @staticmethod
    def get_category_tree(category_id):
        category = get_object_or_404(Category, id = category_id)
        category_list = [category.id]
        children = category.children.all()
        for child in children:
            category_list += CategoryService.get_category_tree(child.id)
        return category_list

class ProductService:
    @staticmethod
    def get_products_by_category(category_id):
        category_id = CategoryService.get_category_tree(category_id)
        products = Product.objects.filter(category__id__in = category_id)
        return products