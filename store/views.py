from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.response import Response

from . import models, serializers


class ProductViewSet(viewsets.ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer

    def destroy(self, request, *args, **kwargs):
        if models.OrderItem.objects.filter(product_id=kwargs["pk"]).count() > 0:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)


class CollectionViewSet(viewsets.ModelViewSet):
    queryset = models.Collection.objects.annotate(products_count=Count("products"))
    serializer_class = serializers.CollectionSerializer

    def destroy(self, request, *args, **kwargs):
        if models.Product.objects.filter(collection=kwargs["pk"]).count() > 0:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)
