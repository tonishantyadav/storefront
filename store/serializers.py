from decimal import Decimal

from django.db import transaction
from rest_framework import serializers

from . import models
from .signals import order_created


class ProductImageSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        product_id = self.context["product_id"]
        return models.ProductImage.objects.create(
            product_id=product_id, **validated_data
        )

    class Meta:
        model = models.ProductImage
        fields = ["id", "image"]


class ProductSerializer(serializers.ModelSerializer):
    price_with_tax = serializers.SerializerMethodField(method_name="calculate_tax")
    images = ProductImageSerializer(many=True, read_only=True)

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
            "images",
        ]


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = ["id", "title", "unit_price"]


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


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, item: models.CartItem):
        return item.product.unit_price * item.quantity

    class Meta:
        model = models.CartItem
        fields = ["id", "product", "quantity", "total_price"]


class AddCartItemSerialzier(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self, value):
        if not models.Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError("No product with given ID was found.")
        return value

    def save(self, **kwargs):
        cart_id = self.context["cart_id"]
        product_id = self.validated_data["product_id"]
        quantity = self.validated_data["quantity"]

        try:
            item = models.CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            item.quantity += quantity
            item.save()
            self.instance = item
        except models.CartItem.DoesNotExist:
            self.instance = models.CartItem.objects.create(
                cart_id=cart_id, **self.validated_data
            )
        return self.instance

    class Meta:
        model = models.CartItem
        fields = ["id", "product_id", "quantity"]


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CartItem
        fields = ["id", "quantity"]


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart: models.Cart):
        return sum(
            [item.product.unit_price * item.quantity for item in cart.items.all()]
        )

    class Meta:
        model = models.Cart
        fields = ["id", "items", "total_price"]


class SimpleCustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    birth_date = serializers.DateField()

    class Meta:
        model = models.Customer
        fields = ["id", "user_id", "phone", "birth_date", "membership"]


class CustomerSerializer(SimpleCustomerSerializer):
    user_id = serializers.IntegerField(read_only=True)


class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()

    class Meta:
        model = models.OrderItem
        fields = ["id", "product", "unit_price", "quantity"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = models.Order
        fields = ["id", "customer", "payment_status", "placed_at", "items"]


class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def validate_cart_id(self, value):
        if not models.Cart.objects.filter(pk=value).exists():
            raise serializers.ValidationError("No cart with given cart ID found.")
        elif models.CartItem.objects.filter(cart_id=value).count() == 0:
            raise serializers.ValidationError("cart is empty.")
        return value

    def save(self, **kwargs):
        with transaction.atomic():
            user_id = self.context["user_id"]
            cart_id = self.validated_data["cart_id"]
            customer = models.Customer.objects.get(user_id=user_id)
            order = models.Order.objects.create(customer=customer)

            cart_items = models.CartItem.objects.select_related("product").filter(
                cart_id=cart_id
            )

            order_items = [
                models.OrderItem(
                    order=order,
                    product=item.product,
                    unit_price=item.product.unit_price,
                    quantity=item.quantity,
                )
                for item in cart_items
            ]

            models.OrderItem.objects.bulk_create(order_items)
            models.Cart.objects.filter(pk=cart_id).delete()
            order_created.send_robust(self.__class__, order=order)
            return order


class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = ["payment_status"]
