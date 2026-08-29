from django.contrib import admin

from . import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "is_active",
        "is_staff",
        "date_joined",
    )
    list_filter = ("is_active", "is_staff", "date_joined",)
    search_fields = ("email",)
    exclude = ("access_token",)

@admin.register(models.Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("email", "phone", "created_at",)
    readonly_fields = ("created_at",)
    search_fields = ("email", "phone",)
    list_display_links= ("email", "phone",)
