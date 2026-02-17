from django.urls import path
from .views import product_detail

app_name = "product"

urlpatterns = [
    path("<int:pk>/", product_detail, name="detail"),
]
