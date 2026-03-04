from django.shortcuts import render, get_object_or_404

from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer

from .models import Product
from .serializers import ProductSerializer

from rest_framework.pagination import PageNumberPagination
from .pagination import ProductPageNumberPagination

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    extras = ["Mouse", "Laptop", "Teclado", "Audífonos", "Multicontactos", "Celular"]

    context = {
        "product": product,
        "extras": extras,
        "divisible_num": 2,
    }
    return render(request, "ecommerce/product_detail.html", context)


class ProductViewSet(ViewSet):
    serializer_class = ProductSerializer
   

    def list(self, request):
        print(">>> list (GET)")

        queryset = Product.objects.all().order_by("-id")

        paginator = ProductPageNumberPagination()
        page = paginator.paginate_queryset(queryset, request)

        results = []
        for p in page:
            results.append({
                "id": p.id,
                "name": p.name,
                "description": p.description,
                "price": str(p.price),
            })

        return paginator.get_paginated_response(results)

    def create(self, request):
        print(">>> create (POST)")
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            p = Product.objects.create(
                name=serializer.validated_data["name"],
                description=serializer.validated_data.get("description", ""),
                price=serializer.validated_data["price"],
            )
            return Response({"message": "Creado", "id": p.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        print(">>> retrieve (GET by id)")
        p = get_object_or_404(Product, pk=pk)
        return Response({
            "message": "Detalle",
            "product": {
                "id": p.id,
                "name": p.name,
                "description": p.description,
                "price": str(p.price),
            }
        })

    def update(self, request, pk=None):
        print(">>> update (PUT)")
        p = get_object_or_404(Product, pk=pk)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            p.name = serializer.validated_data["name"]
            p.description = serializer.validated_data.get("description", "")
            p.price = serializer.validated_data["price"]
            p.save()
            return Response({"message": "Actualizado (PUT)", "id": p.id})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        print(">>> partial_update (PATCH)")
        p = get_object_or_404(Product, pk=pk)

        if "name" in request.data:
            p.name = request.data.get("name")
        if "description" in request.data:
            p.description = request.data.get("description")
        if "price" in request.data:
            p.price = request.data.get("price")

        p.save()
        return Response({"message": "Actualizado (PATCH)", "id": p.id})

    def destroy(self, request, pk=None):
        print(">>> destroy (DELETE)")
        p = get_object_or_404(Product, pk=pk)
        deleted_id = p.id
        p.delete()
        return Response({"message": "Eliminado", "id": deleted_id})