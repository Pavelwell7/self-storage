from django.contrib import admin

from .models import Warehouse
from .models import Box

@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ['city', 'address']
    search_fields = ['city', 'address']

@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    list_display = ['number', 'warehouse', 'price_per_month', 'size']
    list_filter = ['is_occupied']