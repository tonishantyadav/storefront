from django.db.models import Count
from rest_framework import status, viewsets
from rest_framework.response import Response

from . import models, serializers


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ProductSerializer

    def get_queryset(self):
        queryset = models.Product.objects.all()
        collection_id = self.request.query_params.get("collection_id")

        if collection_id is not None:
            queryset = models.Product.objects.filter(collection_id=collection_id)
        return queryset

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


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ReviewSerializer

    def get_queryset(self):
        return models.Review.objects.filter(product_id=self.kwargs["product_pk"])

    def get_serializer_context(self):
        return {"product_id": self.kwargs["product_pk"]}
