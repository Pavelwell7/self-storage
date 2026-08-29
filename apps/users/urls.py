from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("profile/", views.profile_view, name="profile"),
    path("feedback/", views.feedback_view, name="feedback"),
]
