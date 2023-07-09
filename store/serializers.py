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


class ReviewSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        product_id = self.context["product_id"]
        return models.Review.objects.create(product_id=product_id, **validated_data)

    class Meta:
        model = models.Review
        fields = ["id", "name", "description", "date"]


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = models.Cart
        fields = ["id", "created_at"]
