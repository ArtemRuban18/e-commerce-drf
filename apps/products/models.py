from django.db import models
from slugify import slugify

class Category(models.Model):
    name = models.CharField(max_length = 255, null = False, blank = False)
    slug = models.SlugField(max_length = 255, unique = True)
    parent = models.ForeignKey('self', on_delete = models.CASCADE,
                                blank = True,
                                null = True,
                                related_name = 'children')
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']


    def __str__(self):
        return self.name

    def save(self):
        if not self.slug:
            self.slug = slugify.slugify(self.name)
        return super().save()

class InStockProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status = Product.Status.IN_STOCK)
class Product(models.Model):
    class Status(models.TextChoices):
        IN_STOCK = 'in_stock', 'In Stock'
        OUT_OF_STOCK = 'out_of_stock', 'Out of Stock'

    name = models.CharField(max_length = 255, null = False, blank = False)
    slug = models.SlugField(max_length = 255, unique = True)
    description = models.TextField(null = False, blank = False)
    category = models.ForeignKey(Category, on_delete = models.CASCADE, related_name = 'products')
    status = models.CharField(max_length = 15, choices = Status.choices, default = Status.IN_STOCK)
    price = models.DecimalField(max_digits = 10, decimal_places = 2, null = False, blank = False)
    quantity = models.PositiveIntegerField(null = False, blank = False)
    
    objects = models.Manager()
    in_stock = InStockProductManager()

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields = ['name']),
            models.Index(fields = ['slug']),
            models.Index(fields = ['status']),
        ]

    def __str__(self):
        return self.name

    def save(self):
        if not self.slug:
            self.slug = slugify.slugify(self.name)
        if self.quantity == 0:
            self.status = Product.Status.OUT_OF_STOCK
        else:
            self.status = Product.Status.IN_STOCK
        return super().save()

class PhotoProduct(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE, related_name = 'photos')
    image = models.ImageField(upload_to = 'products/photos/')
    is_main = models.BooleanField(default = False)

    class Meta:
        verbose_name = 'Photo Product'
        verbose_name_plural = 'Photo Products'

    def __str__(self):
        return f"Photo of {self.product.name}"