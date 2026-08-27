from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import UserProfileForm


@login_required
def profile_view(request):
    user = request.user

    has_rent = False  # TO DO добавить проверку аренды

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
    return render(request, template, {"form": form, "user": user})
