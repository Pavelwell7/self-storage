from django.contrib import admin
from . import models


@admin.register(models.PromoLink)
class PromoAdmin(admin.ModelAdmin):
    list_display = ()