from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.viewsets import ModelViewSet

from .filters import ProductFilter
from .models import Product
from .pagination_classes import HundredResultsSetPagination
from .serializers import ProductSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all().order_by('name')
    serializer_class = ProductSerializer
    pagination_class = HundredResultsSetPagination
    filterset_class = ProductFilter

    @action(methods=['delete'], detail=False)
    def delete_all(self, request):
        Product.objects.all().delete()
        return Response(status=HTTP_204_NO_CONTENT)





