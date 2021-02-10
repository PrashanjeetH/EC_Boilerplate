from django.shortcuts import render
from django.contrib import messages
from django.views.generic import TemplateView, ListView, DetailView
from core.models import Item, Order, OrderItem
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
# Create your views here.


class Homeview(ListView):
    template_name = 'core/home-page.html'
    model = Item
    context_object_name = 'items'
    extra_context = {
        'title': 'Products',
    }


class ItemDetailView(DetailView):
    model = Item
    template_name = 'core/product.html'


def checkout(requests):
    context = {
        'items': Item.objects.all(),
        'title': 'Checkout',
    }
    return render(requests, "core/checkout-page.html", context=context)


def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False,
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity updated")
        else:
            messages.info(request, "This item added to your cart")
            order.items.add(order_item)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user,
                                     ordered_date=ordered_date)
        order.items.add(order_item)
        messages.success(request, "This item added to your cart")
    return redirect('core:products', slug=slug)


def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user,
                                    ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.get(
                item=item,
                user=request.user,
                ordered=False,
            )
            order.items.remove(order_item)
            messages.success(request, "This item is removed from your cart")
            return redirect('core:products', slug=slug)
        else:
            messages.warning(request, "This item is not in your cart")
            return redirect("core:products", slug=slug)
    else:
        messages.error(request, "You do not have an active order.")
        messages.error(request, "You do not have an active order.")
        return redirect('core:products', slug=slug)
