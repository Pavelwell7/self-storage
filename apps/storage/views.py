from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Max, Min, Prefetch, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .models import Box, Order, Warehouse


def boxes_view(request):
    warehouses = Warehouse.objects.annotate(
        total_boxes=Count("boxes"),
        free_boxes=Count("boxes", filter=Q(boxes__is_occupied=False)),
        min_price=Min("boxes__price_per_month"),
        max_height=Max("boxes__height"),
    ).prefetch_related(
        Prefetch("boxes", queryset=Box.objects.filter(is_occupied=False))
    )

    context = {
        "warehouses": warehouses,
    }
    return render(request, "boxes.html", context)


def index(request):
    return render(request, "index.html")


def faq_view(request):
    return render(request, "faq.html")


def extend_order(request, box):
    order = Order.objects.filter(box=box, user=request.user).filter(
        Q(status='active') | Q(status='expired')
    ).first()
    if not order:
        messages.error(request, "Активная аренда для этого бокса не айдена")
        return redirect("users:profile")
    if order.status == 'expired':
        order.status = 'active'
        box.is_occupied = True
        box.save()
    else:
        if not box.is_occupied:
            box.is_occupied = True
            box.save()
    if request.method == "POST":
        new_end_str = request.POST.get('end_date')
        try:
            new_end_date = datetime.strptime(new_end_str, "%Y-%m-%d").date()
            if new_end_date <= order.end_date:
                raise ValueError
        except:
            messages.error(request, "Дата продления не может быть меньше или равна текущей даты, попробуйте снова")
            return render(
                request, 
                "storage/order_form.html",
                {
                    "box": box,
                    "start_date": order.end_date.isoformat(),
                    "end_date": new_end_str,
                    "extend": True,
                })
        order.end_date = new_end_date
        order.save()
        messages.success(request, f"Аренда успешно продлена до {new_end_str}")
        return redirect("users:profile")
    return render(
        request,
        'storage/order_form.html',
        {
            "box": box,
            "start_date": order.end_date.isoformat(),
            "end_date": (order.end_date + timezone.timedelta(days=30)).isoformat(),
            "extend": True,
        })

@login_required
def order_create(request, box_id):
    box = get_object_or_404(Box, id=box_id)
    is_extend = request.GET.get('extend')
    if is_extend:
        return extend_order(request, box)
    if box.is_occupied:
        messages.error(request, "Бокс занят")
        return redirect("storage:index")
    if request.method == "POST":
        start = request.POST.get("start_date")
        end = request.POST.get("end_date")
        try:
            start_date = datetime.strptime(start, "%Y-%m-%d").date()
            end_date = datetime.strptime(end, "%Y-%m-%d").date()
            if end_date <= start_date:
                raise ValueError
        except:
            messages.error(request, "Неверные даты")
            return render(request, "storage/order_form.html", {"box": box})
        order = Order(
            user=request.user,
            box=box,
            price_per_month=box.price_per_month,
            start_date=start_date,
            end_date=end_date,
            status="active",
        )
        order.save()
        box.is_occupied = True
        box.save()
        messages.success(request, "Аренда оформлена")
        return redirect("users:profile")
    today = timezone.now().date()
    return render(
        request,
        "storage/order_form.html",
        {
            "box": box,
            "start_date": today.isoformat(),
            "end_date": (today + timezone.timedelta(days=30)).isoformat(),
            "extend": False,
        },
    )


