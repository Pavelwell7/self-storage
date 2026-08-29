from django.contrib import admin

from .models import Warehouse
from .models import Box, Order
from .services import update_box_size_and_price


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('city', 'address', 'price_per_square_meter', 'temperature',)
    search_fields = ('city', 'address',)
    list_filter = ('city',)
    list_editable = ('price_per_square_meter', 'temperature',)

@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    list_display = ('number', 'warehouse', 'price_per_month', 'size',)
    list_filter = ('is_occupied',)
    search_fields = ('number', 'warehouse', 'price_per_month',)
    list_display_links = ('number', 'warehouse',)
    readonly_fields = ('price_per_month', 'size')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        update_box_size_and_price(obj)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'user_phone','box', 'start_date', 'end_date', 'status', 'total_price')
    list_filter = ('status', 'box__warehouse')
    search_fields = ('user__username', 'box__number')
    readonly_fields = ('total_price',)
    ordering = ('-start_date',)
    list_display_links = ('user',)

    def user_phone(self, obj):
        phone = obj.user.phone
        if phone:
            try:
                if hasattr(phone, 'as_national'):
                    return str(phone.as_national())
                else:
                    return str(phone)
            except Exception:
                return str(phone)
        return "-"
    user_phone.short_description = "Телефон"
