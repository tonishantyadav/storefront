from rest_framework import serializers
from . import models

class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = ["id", "title", "unit_price"]