from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.storage.models import Order


class Command(BaseCommand):
    help = "J,yjdkztn ghjchjxtyyst pfrrfps"

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        expired_orders = Order.objects.filter(status = 'active', end_date__lt=today)
        count_order = expired_orders.count()
        if count_order == 0:
            self.stdout.write(self.style.WARNING('Нет просроченных заказов'))
            return
        expired_orders.update(status='expired')
        self.stdout.write(self.style.SUCCESS('Статусы обновлены'))