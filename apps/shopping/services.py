from apps.products.models import Product
from rest_framework.exceptions import ValidationError
from typing import Dict, Optional


class ShoppingService:
    def __init__(self, session, key: str) -> None:
        self.session = session
        self.key = key

    def get(self) -> Dict:
        """Отримати дані з сесії."""
        return self.session.get(self.key, {})

    def save(self, data: Dict) -> None:
        """Зберегти дані в сесію."""
        self.session[self.key] = data
        self.session.modified = True
    
    def clear(self) -> None:
        self.save({})
    

class CartService:
    
    def __init__(self, shopping: ShoppingService) -> None:
        self.shopping = shopping
        self.items = shopping.get()
    
    def add(self, product_id: int, quantity: int = 1) -> None:

        if not Product.objects.filter(id=product_id).exists():
            raise ValidationError("Product doesn't exists")
        product_id = str(product_id)

        self.items[product_id] = (self.items.get(product_id, 0) + quantity)

        self.shopping.save(self.items)

    def update(self, product_id: int, quantity: int) -> None:
        if not Product.objects.filter(id=product_id).exists():
            raise ValidationError("Product doesn't exists")
        product_id = str(product_id)

        if product_id not in self.items:
            raise ValidationError("Product not in cart")
    
        self.items[product_id] = quantity
        self.shopping.save(self.items)

    
    def remove(self, product_id: int) -> None:
        self.items.pop(str(product_id), None)
        self.shopping.save(self.items)
    
    def clear(self) -> None:
        self.shopping.clear()
        self.items = {}
    
    def get_items(self) -> Dict[str, int]:
        return self.items


class WishlistService:
    def __init__(self, shopping: ShoppingService) -> None:
        self.shopping = shopping
        self.items = shopping.get()
    
    def add(self, product_id: int) -> None:
        if not Product.objects.filter(id=product_id).exists():
            raise ValidationError("Product doesn't exists")
        product_id = str(product_id)

        self.items[product_id] = 1

        self.shopping.save(self.items)

    
    def remove(self, product_id: int) -> None:
        self.items.pop(str(product_id), None)

        self.shopping.save(self.items)

    def clear(self) -> None:
        self.shopping.clear()
        self.items = {}

    def get_items(self) -> Dict[str, int]:
        return self.items