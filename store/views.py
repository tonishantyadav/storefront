from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework import permissions as BasePermissions
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response

from . import filters, models, permissions, serializers


class ProductViewSet(viewsets.ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = filters.ProductFilter
    search_fields = ["title", "description"]
    ordering_fields = ["unit_price", "last_update"]
    permission_classes = [permissions.IsAdminOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        if models.OrderItem.objects.filter(product_id=kwargs["pk"]).count() > 0:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)


class CollectionViewSet(viewsets.ModelViewSet):
    queryset = models.Collection.objects.annotate(products_count=Count("products"))
    serializer_class = serializers.CollectionSerializer
    permission_classes = [permissions.IsAdminOrReadOnly]

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


class CartViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = models.Cart.objects.prefetch_related("items__product").all()
    serializer_class = serializers.CartSerializer


class CartItemViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]

    def get_queryset(self):
        return models.CartItem.objects.filter(
            cart_id=self.kwargs.get("cart_pk")
        ).select_related("product")

    def get_serializer_class(self):
        if self.request.method == "POST":
            return serializers.AddCartItemSerialzier
        elif self.request.method == "PUT":
            return serializers.UpdateCartItemSerializer
        return serializers.CartItemSerializer

    def get_serializer_context(self):
        return {
            "cart_id": self.kwargs.get("cart_pk"),
        }


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = models.Customer.objects.all()
    serializer_class = serializers.CustomerSerializer
    permission_classes = [BasePermissions.IsAdminUser]

    @action(
        detail=False,
        methods=["GET", "PUT"],
        permission_classes=[BasePermissions.IsAuthenticated],
    )
    def me(self, request):
        customer, created = models.Customer.objects.get_or_create(
            user_id=self.request.user.id
        )
        if request.method == "GET":
            serializer = serializers.CustomerSerializer(customer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == "PUT":
            serializer = serializers.CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [BasePermissions.IsAuthenticated]

    def get_serializer_context(self):
        return {"user_id": self.request.user.id}

    def get_serializer_class(self):
        if self.request.method == "POST":
            return serializers.CreateOrderSerializer
        return serializers.OrderSerializer

    def get_queryset(self):
        user = self.request.user
        (customer_id, create) = models.Customer.objects.only("pk").get_or_create(
            user_id=user.id
        )
        if user.is_staff:
            return models.Order.objects.prefetch_related("items__product").all()
        return models.Order.objects.prefetch_related("items__product").filter(
            customer_id=customer_id
        )
