from django.urls import path
from core.views import (
    Homeview,
    checkout,
    ItemDetailView,
    add_to_cart,
    remove_from_cart)


app_name = 'core'

urlpatterns = [
    path('', Homeview.as_view(), name='home'),
    path('checkout/', checkout, name='checkout'),
    path('products/<slug>/', ItemDetailView.as_view(), name='products'),
    path('add_to_cart/<slug>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<slug>/', remove_from_cart, name='remove_from_cart'),
]

