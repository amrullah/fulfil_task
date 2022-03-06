from rest_framework.test import APITestCase

from .models import Product


class ProductTests(APITestCase):
    def test_product_creation_and_querying(self):
        product = Product(sku='something', name='Superb', description='Mind Blowing, no words')
        product.save()
        self.assertEqual(Product.objects.count(), 1, msg="One product should have been created")
        # print("\n\n")
        # print(Product.objects.all().explain(verbose=True, analyze=True))
        # print("\n\n")

    def test_product_crud_apis(self):
        url = "/products/"
        data = {
            'sku': 'something',
            'name': 'Something unbelievable',
            'description': 'Mind Blowing, speechless'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assert_('sku' in response.data['results'][0])
        self.assertEqual(response.data['count'], 1)

        response = self.client.get(url + "something/", format='json')
        self.assert_('sku' in response.data)

        data = {
            'description': 'Something you can\'t believe'
        }
        response = self.client.patch(url + "something/", data, format='json')
        self.assertEqual(response.status_code, 200)

        response = self.client.get(url + "something/", format='json')
        self.assertEqual(response.data['description'], 'Something you can\'t believe')

        data = {
            'sku': 'something-else',
            'name': 'mind boggling',
            'description': 'itna mast ke poocho mat'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)

        response = self.client.get(url, format='json')
        self.assertEqual(response.data['count'], 2)

        self.client.delete(url + "something/", format='json')

        response = self.client.get(url, format='json')
        self.assertEqual(response.data['count'], 1)

        self.client.delete(url + "delete_all/", format='json')

        response = self.client.get(url, format='json')
        self.assertEqual(response.data['count'], 0)


