from django.test import TestCase

from .models import PromoLink


class PromoLinkManagerTest(TestCase):
    def setUp(self):
        # Создаём активную ссылку
        self.active_link = PromoLink.objects.create(
            promo_link="test_active",
            origin_link="http://example.com",
            is_active=True,
            clicks_count=0,
        )
        # Создаём неактивную ссылку
        self.inactive_link = PromoLink.objects.create(
            promo_link="test_inactive",
            origin_link="http://example.com",
            is_active=False,
            clicks_count=0,
        )

    def test_increment_active_link(self):
        """При переходе по активной ссылке счётчик увеличивается и возвращается объект"""
        link = PromoLink.objects.increment_and_get("test_active")
        self.assertIsNotNone(link)
        self.assertEqual(link.clicks_count, 1)  # счётчик увеличился
        self.assertEqual(link.promo_link, "test_active")

    def test_increment_inactive_link(self):
        """При переходе по неактивной ссылке возвращается None, счётчик не меняется"""
        link = PromoLink.objects.increment_and_get("test_inactive")
        self.assertIsNone(link)
        # Проверяем, что счётчик не изменился
        self.assertEqual(
            PromoLink.objects.get(promo_link="test_inactive").clicks_count, 0
        )

    def test_increment_nonexistent_link(self):
        """При переходе по несуществующей ссылке возвращается None"""
        link = PromoLink.objects.increment_and_get("nonexistent")
        self.assertIsNone(link)
