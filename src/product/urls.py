from django.urls import path
from .views import product_detail, ProductAPIView

app_name = "product"

urlpatterns = [
    path("<int:pk>/", product_detail, name="detail"),
    path("api/", ProductAPIView.as_view(), name="api"),
]