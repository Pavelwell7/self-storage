from django.db import models
from django.db.models import F


class PromoLinkManager(models.Manager):
    def create_link(
        self,
        promo_title,
        origin_link,
        referrer="",
        is_active=True,
    ):
        promo = self.create(
            promo_title=promo_title,
            origin_link=origin_link,
            referrer=referrer,
            is_active=is_active,
        )
        base = promo_title.strip()
        promo.promo_link = f"{base}_{promo.id}"
        promo.save(update_fields=["promo_link"])
        return promo

    def increment_and_get(self, promo_link):
        updated = self.filter(promo_link=promo_link, is_active=True).update(
            clicks_count=F("clicks_count") + 1
        )
        if updated:
            return self.get(promo_link=promo_link)
        return None


class PromoLink(models.Model):
    referrer = models.CharField("Реферер", max_length=150, blank=True)
    origin_link = models.URLField(
        "Оригинальная ссылка",
    )
    promo_title = models.CharField(
        "Промо заголовок",
        max_length=150,
        default="",
    )
    promo_link = models.CharField(
        "Промо ссылка",
        max_length=20,
        unique=True,
        db_index=True,
    )
    created_at = models.DateTimeField(
        "Дата создания ссылки",
        auto_now_add=True,
    )
    clicks_count = models.IntegerField(
        "Количество кликов",
        default=0,
    )
    is_active = models.BooleanField(
        "Активность ссылки",
        default=True,
    )
    objects = PromoLinkManager()

    class Meta:
        verbose_name = "Промо ссылка"
        verbose_name_plural = "Промо ссылки"
        ordering = ("-created_at",)

    def __str__(self):
        return f"/{self.promo_link} ({self.referrer}) → {self.clicks_count} кликов"
