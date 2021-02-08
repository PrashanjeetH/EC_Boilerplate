from django.contrib import admin
from core.models import *
# Register your models here.


@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    list_display = ['title', 'price', 'category', 'seller', 'date_modified']
    list_per_page = 40
    search_fields = ['title', 'category', 'seller']


@admin.register(Category)
class AdminProduct(admin.ModelAdmin):
    list_display = ['name']
    # list_display_links = ['name']
    # list_editable = ('name',)
    list_per_page = 40
    search_fields = ['name']


@admin.register(Label)
class AdminProduct(admin.ModelAdmin):
    list_display = ['name']
    list_per_page = 40
    search_fields = ['name']


@admin.register(Address)
class AdminProduct(admin.ModelAdmin):
    list_display = ['user', 'address_type']
    list_per_page = 40
    search_fields = ['user']


@admin.register(Vendor)
class AdminProduct(admin.ModelAdmin):
    list_display = ['user']
    list_per_page = 40
    search_fields = ['user']
