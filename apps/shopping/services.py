from apps.products.models import Product
from decimal import Decimal
from rest_framework.exceptions import ValidationError

class ShoppingService:
    def __init__(self, request, key):
        self.session = request.session
        self.key = key
        self.items = self.session.get(key, {})

    def save(self):
        self.session[self.key] = self.items
        self.session.modified = True
    
    def remove(self, product_id):
        product_id = str(product_id)
        self.items.pop(product_id, None)

        self.save()
    
    def clear(self):
        self.items = {}
        self.save()
    
    def __len__(self):
        return sum(self.items.values())

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

    def update(self, product_id, quantity):
        product_id = str(product_id)

        if product_id not in self.items:
            raise ValidationError("Product isn't in cart")
    
        self.items[product_id] = quantity

        self.save()
    
    def get_total_price(self):
        products_ids = self.items.keys()

        products = Product.objects.filter(id__in = products_ids)

        total = Decimal("0")

        for product in products:
            quantity = self.items[str(product.id)]
            total += product.price * quantity
        
        return total
    
class WishlistService(ShoppingService):
    def __init__(self, request):
        super().__init__(request, "wishlist")
    
    def add(self, product_id):
        product_id = str(product_id)

        if product_id in self.items:
            self.remove(product_id)
        else:
            self.items[product_id] = 1
            
        self.save()