from django.urls import path
from . import views

app_name = 'storage'

urlpatterns = [
  path('', views.index, name='index'),
  path('boxes/', views.boxes_view, name='boxes'),
  path('faq/', views.faq_view, name='faq'),
]