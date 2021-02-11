from django.shortcuts import render
from django.contrib import messages
from django.views.generic import TemplateView, ListView, DetailView, View
from core.models import Item, Order, OrderItem
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


class Homeview(ListView):
    paginate_by = 2
    template_name = 'core/home-page.html'
    model = Item
    context_object_name = 'items'
    extra_context = {
        'title': 'Products',
    }


class ItemDetailView(DetailView):
    model = Item
    template_name = 'core/product.html'


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            return render(self.request, 'core/ordersummary.html',
                          context={'object': order})
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have any item in cart")
            return redirect('/')

    model = Order
    template_name = 'core/ordersummary.html'


@login_required
def checkout(requests):
    context = {
        'items': Item.objects.all(),
        'title': 'Checkout',
    }
    return render(requests, "core/checkout-page.html", context=context)


@login_required
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
            return redirect('core:order-summary')
        else:
            messages.info(request, "This item added to your cart")
            order.items.add(order_item)
            return redirect('core:order-summary')
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user,
                                     ordered_date=ordered_date)
        order.items.add(order_item)
        messages.success(request, "This item added to your cart")
    return redirect('core:order-summary')


@login_required
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
            return redirect('core:order-summary')
        else:
            messages.warning(request, "This item is not in your cart")
            return redirect("core:order-summary")
    else:
        messages.error(request, "You do not have an active order.")
        return redirect('core:order-summary')


@login_required
def remove_item_from_cart(request, slug):
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
            if order_item.quantity > 0:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.success(request, "This item is removed from your cart")
            return redirect('core:order-summary')
        else:
            messages.warning(request, "This item is not in your cart")
            return redirect("core:order-summary")
    else:
        messages.error(request, "You do not have an active order.")
        return redirect('core:order-summary')
