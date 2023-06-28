from django.contrib import admin
from . import models


# Admin model that represents Product model in admin site
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    # Properties that applied on Admin model
    list_display = ["title", "unit_price"]
    list_editable = ["unit_price"]
    list_per_page = 20


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ["title", "featured_product"]


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "membership"]
    list_editable = ["membership"]
    ordering = ["first_name", "last_name"]
    list_per_page = 20
