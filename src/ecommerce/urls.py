from django.urls import path
from .views import (
    VentasHomeView,
    AddToCartView,
    RemoveFromCartView,
    ClearCartView,
    CheckoutView,
)

app_name = "ventas"

urlpatterns = [
    path("", VentasHomeView.as_view(), name="ventas-home"),
    path("cart/add/<int:product_id>/", AddToCartView.as_view(), name="add-to-cart"),
    path("cart/remove/<int:product_id>/", RemoveFromCartView.as_view(), name="remove-from-cart"),
    path("cart/clear/", ClearCartView.as_view(), name="clear-cart"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
]
