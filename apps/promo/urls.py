from django.urls import path

from . import views

app_name = "promo"

urlpatterns = [
    path("go/<str:promo_link>/", views.go_to_promo, name="go_to_promo"),
]
