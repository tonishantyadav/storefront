from django.urls import path
from rest_framework_nested import routers

from . import views

router = routers.DefaultRouter()

router.register("collections", views.CollectionViewSet)
router.register("customers", views.CustomerViewSet)

router.register("products", views.ProductViewSet, basename="products")
products_router = routers.NestedDefaultRouter(router, "products", lookup="product")
products_router.register("reviews", views.ReviewViewSet, basename="product-reviews")

router.register("carts", views.CartViewSet)
carts_router = routers.NestedDefaultRouter(router, "carts", lookup="cart")
carts_router.register("items", views.CartItemViewSet, basename="cart-items")


urlpatterns = router.urls + products_router.urls + carts_router.urls
