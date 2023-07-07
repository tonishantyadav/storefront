from django.urls import path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register("products", views.ProductViewSet)
router.register("collections", views.CollectionViewSet)

urlpatterns = router.urls