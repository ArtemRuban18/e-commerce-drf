from apps.products.models import Product
from decimal import Decimal

def get_cart_products(cart_items: dict[str, int]) -> dict[str, int]:
    products = Product.objects.filter(id__in=cart_items.keys())

    items = []

    total = Decimal("0")

    for product in products:
        quantity = cart_items[str(product.id)]

        product_total = product.price * quantity

        items.append({
                "id": product.id,
                "name": product.name,
                "price": product.price,
                "quantity": quantity,
                "total_price": product_total
            })
        
        total += product_total

    return {
        "items": items,
        "total_price": total,
        "total_quantity": sum(cart_items.values())
    }

def get_wishlist_products(wishlist_items:dict[str, int]) -> dict[str, int]:
    products = Product.objects.filter(id__in=wishlist_items.keys())

    items = []

    for product in products:
        items.append(
            {
            "name": product.name,
            "price":product.price
            }
        )
    
    return {
        "items": items,
        "product_count": products.count()
    }