from products.models import Product


class ProductCreator:
    @staticmethod
    def create(name: str, sku: str, description: str) -> Product:
        try:
            product = Product.objects.get(sku=sku.lower())
        except Product.DoesNotExist:
            product = Product(sku=sku.lower())

        product.name = name
        product.description = description

        product.save()

        return product

