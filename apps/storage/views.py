from django.db.models import Count, Q, Min, Max
from django.shortcuts import render
from .models import Warehouse


def boxes_view(request):
    warehouses = Warehouse.objects.annotate(
        total_boxes=Count('boxes'),
        free_boxes=Count('boxes', filter=Q(boxes__is_occupied=False)),
        min_price=Min('boxes__price_per_month'),
        max_height=Max('boxes__height')
    ).prefetch_related('boxes')

    context = {
        'warehouses': warehouses,
    }
    return render(request, 'boxes.html', context)

def index(request):
    return render(request, 'index.html')


def faq_view(request):
    return render(request, 'faq.html')