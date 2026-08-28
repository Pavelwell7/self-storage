from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone

from .forms import UserProfileForm


@login_required
def profile_view(request):

    user = request.user
    orders = request.user.orders.select_related("box__warehouse").order_by(
        "-start_date"
    )
    for order in orders:
        days_left = (order.end_date - timezone.now().date()).days
        order.is_expiring_soon = days_left <= 14

    has_rent = orders.exists()

    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Профиль успешно обновлён")
            return redirect("users:profile")
    else:
        form = UserProfileForm(instance=user)
        for field in form.fields.values():
            field.widget.attrs["disabled"] = "disabled"

    template = "my-rent.html" if has_rent else "my-rent-empty.html"
    return render(request, template, {"form": form, "user": user, "orders": orders})
