from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.http import HttpResponseNotAllowed

from .models import Product  

from django.http import JsonResponse
from django.views import View
from order_manager.models import Order
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import UserRegisterForm


def register(request):
    initial_data = {
        "username": "usuario_demo",
        "email": "correo@demo.com",
    }

    form = UserRegisterForm(
        request.POST or None,
        initial=initial_data
    )

    if form.is_valid():
        form.save()
        messages.success(request, "Usuario creado correctamente")
        return redirect("ecommerce:home") 

    return render(request, "ecommerce/register.html", {
        "form": form
    })
class VentasAjaxView(View):
    def get(self, request, *args, **kwargs):
        qs = Order.objects.order_by("-created_at")[:10]

        labels = []
        data = []

        for order in qs:
            labels.append(f"Orden #{order.id}")
            data.append(float(order.total)) 

        return JsonResponse({"labels": labels, "data": data})

class VentasHomeView(View):
    template_name = "ecommerce/ventas.html"

    def get_cart_context(self, request):
        cart = request.session.get("cart", {}) 
        cart_items = []
        total = 0.0

        for pid_str, qty in cart.items():
            product = get_object_or_404(Product, id=int(pid_str))
            subtotal = float(product.price) * int(qty)
            total += subtotal
            cart_items.append({
                "product": product,
                "qty": int(qty),
                "subtotal": subtotal,
            })

        return cart_items, total

    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        cart_items, total = self.get_cart_context(request)

        context = {
            "products": products,
            "cart_items": cart_items,
            "cart_total": total,
        }
        return render(request, self.template_name, context)


class AddToCartView(View):
    def post(self, request, product_id, *args, **kwargs):
        product = get_object_or_404(Product, id=product_id)

        cart = request.session.get("cart", {})
        pid = str(product.id)
        cart[pid] = cart.get(pid, 0) + 1

        request.session["cart"] = cart
        request.session.modified = True

        messages.success(request, f"Agregaste '{product.title}' al carrito.")
        return redirect("ventas:ventas-home")

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(["POST"])


class RemoveFromCartView(View):
    def post(self, request, product_id, *args, **kwargs):
        cart = request.session.get("cart", {})
        pid = str(product_id)

        if pid in cart:
            cart[pid] -= 1
            if cart[pid] <= 0:
                del cart[pid]

        request.session["cart"] = cart
        request.session.modified = True
        return redirect("ventas:ventas-home")

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(["POST"])


class ClearCartView(View):
    def post(self, request, *args, **kwargs):
        request.session["cart"] = {}
        request.session.modified = True
        messages.info(request, "Carrito vaciado.")
        return redirect("ventas:ventas-home")

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(["POST"])


class CheckoutView(View):
    def post(self, request, *args, **kwargs):
        cart = request.session.get("cart", {})
        if not cart:
            messages.error(request, "Tu carrito está vacío.")
            return redirect("ventas:ventas-home")

        
        request.session["cart"] = {}
        request.session.modified = True
        messages.success(request, "Pedido procesado correctamente ")
        return redirect("ventas:ventas-home")

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(["POST"])
