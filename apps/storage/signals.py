from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Order, Box


@receiver(pre_save, sender=Order)
def calculate_total_price(sender, instance, **kwargs):
    if instance.start_date and instance.end_date and not instance.total_price:
        months = (instance.end_date.year - instance.start_date.year) * 12 + (instance.end_date.month - instance.start_date.month)
        months = max(1, months)
        instance.total_price = instance.price_per_month * months

@receiver(post_delete, sender=Order)
def release_box_on_delete(sender, instance, **kwargs):
	box = instance.box
	if not sender.objects.filter(box=box, status='active').exists():
		box.is_occupied = False
		box.save()

@receiver(post_save, sender=Order)
def release_box_onstatus_change(sender, instance, **kwargs):
    box = instance.box
    if instance.status == 'active':
        box.is_occupied = True
        box.save()
    else: 
        if not sender.objects.filter(box=box, status__in=('active', 'expired')).exists():
            box.is_occupied = False
            box.save()
