from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import datetime
from .models import Box, Order

def index(request):
    return render(request, 'index.html')

def boxes_view(request):
  return render(request, 'boxes.html')

def faq_view(request):
  return render(request, 'faq.html')

@login_required
def order_create(request, box_id):
    box = get_object_or_404(Box, id=box_id)
    if box.is_occupied:
        messages.error(request, "Бокс занят")
        return redirect('storage:index')
    if request.method == 'POST':
        start = request.POST.get('start_date')
        end = request.POST.get('end_date')
        try:
            start_date = datetime.strptime(start, '%Y-%m-%d').date()
            end_date = datetime.strptime(end, '%Y-%m-%d').date()
            if end_date <= start_date:
                raise ValueError
        except:
            messages.error(request, 'Неверные даты')
            return render(request, 'storage/order_form.html', {'box': box})
        order = Order(
            user=request.user,
            box=box,
            price_per_month=box.price_per_month,
            start_date=start_date,
            end_date=end_date,
            status='active'
        )
        order.save()
        box.is_occupied = True
        box.save()
        messages.success(request, 'Аренда оформлена')
        return redirect('storage:profile')
    today = timezone.now().date()
    return render(request, 'storage/order_form.html', {
        'box': box,
        'start_date': today.isoformat(),
        'end_date': (today + timezone.timedelta(days=30)).isoformat(),
    })