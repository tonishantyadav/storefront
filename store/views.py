from rest_framework.decorators import api_view
from rest_framework.response import Response

from . import models
from . import serializers


@api_view()
def product_list(request):
    return Response("ok")


@api_view()
def product_detail(request, pk):
    product = models.Product.objects.get(pk=pk)
    serializer = serializers.ProductSerializer(product)
    return Response(data=serializer.data)
