from django.shortcuts import render, get_object_or_404
from .models import Product

from rest_framework import views
from rest_framework.response import Response


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    extras = ["Mouse", "Laptop", "Teclado", "Audífonos", "Multicontactos", "Celular"]

    context = {
        "product": product,
        "extras": extras,
        "divisible_num": 2,
    }
    return render(request, "ecommerce/product_detail.html", context)


class ProductAPIView(views.APIView):

    def get(self, request):
        print(">>> Estás llamando el método GET")
        return Response({"message": "Estás llamando el método GET"})

    def post(self, request):
        print(">>> Estás llamando el método POST")
        return Response({"message": "Estás llamando el método POST"})

    def put(self, request):
        print(">>> Estás llamando el método PUT")
        return Response({"message": "Estás llamando el método PUT"})

    def patch(self, request):
        print(">>> Estás llamando el método PATCH")
        return Response({"message": "Estás llamando el método PATCH"})

    def delete(self, request):
        print(">>> Estás llamando el método DELETE")
        return Response({"message": "Estás llamando el método DELETE"})