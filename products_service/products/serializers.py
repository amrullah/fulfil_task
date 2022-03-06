from rest_framework.serializers import HyperlinkedModelSerializer

from .models import Product


class ProductSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ['sku', 'name', 'is_active', 'description', 'url']
