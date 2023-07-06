from decimal import Decimal

from rest_framework import serializers

from . import models


class CollectionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)


class ProductSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(6, 2, source="unit_price")
    price_with_tax = serializers.SerializerMethodField(method_name="calculate_tax")
    collection = CollectionSerializer()

    def calculate_tax(self, product: models.Product):
        return product.unit_price * Decimal(1.1)

    class Meta:
        model = models.Product
        fields = ["id", "title", "price", "price_with_tax", "collection"]
