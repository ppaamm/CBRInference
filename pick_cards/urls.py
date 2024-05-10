from django.urls import path

from . import views

app_name = "pick_cards"

urlpatterns = [
    path("", views.index, name="index"),
]