from django.test import TestCase

from .models import Product


class ProductTests(TestCase):
    def test_product_creation_and_querying(self):
        product = Product(sku='something', name='Superb', description='Mind Blowing, no words')
        product.save()
        self.assertEqual(Product.objects.count(), 1, msg="One product should have been created")
        print("\n\n")
        print(Product.objects.all().explain(verbose=True, analyze=True))
        print("\n\n")