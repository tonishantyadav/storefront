from django.shortcuts import render
from store.models import Product


def say_hello(request):
    queryset = Product.objects.select_related("collection").all()
    return render(request, "hello.html", {"name": "Nishant", "products": queryset})
