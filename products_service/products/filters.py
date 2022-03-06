from django_filters.rest_framework import FilterSet, CharFilter

from .models import Product


class ProductFilter(FilterSet):
    sku = CharFilter(lookup_expr='exact')
    name = CharFilter(lookup_expr='istartswith')
    description = CharFilter(lookup_expr='search')

    class Meta:
        model = Product
        fields = ['sku', 'name', 'is_active', 'description']
