from django.urls import path

from . import views

app_name = "ai_process"

urlpatterns = [
    path("", views.index, name="index"),
    path("index", views.index, name="index"),
    path("index/<str:session_id>/<int:quiz_id>", views.index, name="index"),
    path("display_results/<str:session_id>/<int:quiz_id>/<str:predictions>/<str:recommendations>", views.display_results, name="display_results"),
]