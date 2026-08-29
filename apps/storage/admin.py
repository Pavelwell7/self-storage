from django.contrib import admin

from .models import Warehouse
from .models import Box, Order

@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ['city', 'address']
    search_fields = ['city', 'address']

@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    list_display = ['number', 'warehouse', 'price_per_month', 'size']
    list_filter = ['is_occupied']
    search_fields = ['number', 'warehouse', 'price_per_month']
    list_display_links = ['number', 'warehouse',]
    readonly_fields = ('price_per_month', 'size')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'user_phone','box', 'start_date', 'end_date', 'status', 'total_price')
    list_filter = ('status', 'box__warehouse')
    search_fields = ('user__username', 'box__number')
    readonly_fields = ('total_price',)
    ordering = ('-start_date',)
    list_display_links = ('user',)

    def user_phone(self, obj):
        if obj.user.phone:
            return obj.user.phone.as_national()
        return "-"
    user_phone.short_description = "Телефон"

