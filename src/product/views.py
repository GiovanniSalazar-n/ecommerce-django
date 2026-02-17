from django.shortcuts import render, get_object_or_404
from .models import Product

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    extras = ["Mouse", "Laptop", "Teclado", "Audífonos", "Multicontactos", "Celular"]

    context = {
        "product": product,
        "extras": extras,
        "divisible_num": 2,
    }
    return render(request, "ecommerce/product_detail.html", context)
