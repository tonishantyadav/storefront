from decimal import Decimal

from rest_framework import serializers

from . import models


class ProductSerializer(serializers.ModelSerializer):
    price_with_tax = serializers.SerializerMethodField(method_name="calculate_tax")

    def calculate_tax(self, product: models.Product):
        return product.unit_price * Decimal(1.1)

    class Meta:
        model = models.Product
        fields = [
            "id",
            "title",
            "description",
            "slug",
            "inventory",
            "unit_price",
            "price_with_tax",
            "collection",
        ]


class CollectionSerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.Collection
        fields = ["id", "title", "products_count"]
