from apps.products.models import Product
from decimal import Decimal
from rest_framework.exceptions import ValidationError

class ShoppingService:
    def __init__(self, session, key: str):
        self.session = session
        self.key = key

    def get(self) -> dict:
        return self.session.get(self.key, {})

    def save(self, data: dict) -> None:
        self.session[self.key] = data
        self.session.modified = True
    
    def clear(self) -> None:
        self.save({})
    

class CartService:
    def __init__(self, shopping: ShoppingService):
        self.shopping = shopping
        self.items = shopping.get()
    
    def add(self, product_id: int, quantity: int = 1) -> None:
        product_id = str(product_id)

        self.items[product_id] = (self.items.get(product_id, 0) + quantity)

        self.shopping.save(self.items)

    def update(self, product_id: int, quantity: int) -> None:
        product_id = str(product_id)

        if product_id not in self.items:
            raise ValidationError("Product not in cart")
    
        self.items[product_id] = quantity
        self.shopping.save(self.items)

    
    def remove(self, product_id: int) -> None:
        self.items.pop(str(product_id), None)
        self.shopping.save(self.items)
    
    def clear(self):
        self.shopping.clear()
    
    def get_items(self) -> dict[str, int]:
        return self.items

class WishlistService:
    def __init__(self, shopping: ShoppingService):
        self.shopping = shopping
        self.items = shopping.get()
    
    def add(self, product_id: int):
        product_id = str(product_id)

        self.items[product_id] = 1

        self.shopping.save(self.items)

    
    def remove(self, product_id: int) -> None:
        self.items.pop(str(product_id), None)

        self.shopping.save(self.items)

    def clear(self):
        self.shopping.clear()

    def get_items(self) -> dict[str, int]:
        return self.items