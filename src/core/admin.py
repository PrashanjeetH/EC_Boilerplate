from django.contrib import admin
from core.models import *


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'price']


@admin.register(OrderItem)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['item', 'quantity']


@admin.register(Order)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'ordered_date', 'ordered']
