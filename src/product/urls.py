from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import product_detail, ProductViewSet

app_name = "product"

router = DefaultRouter()
router.register("api/products", ProductViewSet, basename="products")

urlpatterns = [
    path("<int:pk>/", product_detail, name="detail"),
    path("", include(router.urls)),
]