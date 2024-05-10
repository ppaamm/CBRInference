from django.urls import path

from . import views

app_name = "evaluation"

urlpatterns = [
    path('index', views.index, name='index'),
    path('index/<str:session_id>/<int:quiz_id>/<int:round_id>', views.index, name='index'),
]