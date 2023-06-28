from django.contrib import admin
from . import models


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["title", "unit_price", "inventory_status", "collection_title"]
    list_editable = ["unit_price"]
    list_per_page = 20
    list_select_related = ["collection"]

    @admin.display(ordering="inventory")
    def inventory_status(self, product):
        if product.inventory < 10:
            return "Low"
        return "Ok"

    @admin.display(ordering="collection")
    def collection_title(self, product):
        return product.collection.title


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ["title", "featured_product"]


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "membership"]
    list_editable = ["membership"]
    ordering = ["first_name", "last_name"]
    list_per_page = 20


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["customer_name", "placed_at", "payment_status"]
    list_select_related = ["customer"]
    list_per_page = 20

    @admin.display(ordering="customer__first_name")
    def customer_name(self, order):
        return f"{order.customer.first_name} {order.customer.last_name}"
