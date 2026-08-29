from django.http import Http404
from django.shortcuts import redirect
from django.views.decorators.cache import never_cache

from .models import PromoLink


@never_cache
def go_to_promo(request, promo_link):
    link = PromoLink.objects.increment_and_get(promo_link)
    if not link:
        raise Http404("Ссылка не найдена или неактивна")
    return redirect(link.origin_link)
