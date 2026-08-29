from django.contrib import admin
from django.utils.html import format_html

from self_storage import settings

from .models import PromoLink


@admin.register(PromoLink)
class PromoAdmin(admin.ModelAdmin):
    list_display = (
        "promo_link",
        "referrer",
        "clicks_count",
        "created_at",
        "full_link",
        "is_active",
    )
    readonly_fields = (
        "created_at",
        "clicks_count",
        "promo_link",
        "full_link",
    )

    def full_link(self, obj):
        full_url = f"{settings.SITE_URL}/go/{obj.promo_link}"
        return format_html('<a href="{}" target="_blank">{}</a>', full_url, full_url)

    full_link.short_description = "Кликабельная ссылка"

    def save_model(self, request, obj, form, change):
        if not change:
            link = PromoLink.objects.create_link(
                promo_title=obj.promo_title,
                origin_link=obj.origin_link,
                referrer=obj.referrer,
                is_active=obj.is_active,
            )

            obj.pk = link.pk
            obj.promo_link = link.promo_link
            obj.created_at = link.created_at
            obj.clicks_count = link.clicks_count
        else:
            super().save_model(request, obj, form, change)
