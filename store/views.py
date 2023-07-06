from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from . import models, serializers


@api_view()
def product_list(request):
    return Response("ok")


@api_view()
def product_detail(request, pk):
    product = get_object_or_404(models.Product, pk=pk)
    serializer = serializers.ProductSerializer(product)
    return Response(data=serializer.data)
