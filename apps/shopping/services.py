from apps.products.models import Product
from decimal import Decimal


class ShoppingService:
    def __init__(self, request, key):
        self.session = request.session
        self.key = key
        self.items = self.session.get(key, {})
    
    def get_items(self):
        return self.items

    def save(self):
        self.session[self.key] = self. items
        self.session.modified = True
    
    def clear(self):
        self.items = {}
        self.save()
    
    def remove(self, product_id):
        product_id = str(product_id)
        self.items.pop(product_id, None)

        self.save()

class CartService(ShoppingService):
    def __init__(self, request):
        super().__init__(request, "cart")
    
    def add(self, product_id, quantity = 1):
        product_id = str(product_id)

        if product_id in self.items:
            self.items[product_id] += quantity
        
        else:
            self.items[product_id] = quantity

        self.save()

    