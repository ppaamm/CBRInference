"""
URL configuration for CBRInference project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("intro/", include("intro.urls", namespace="intro")),
    path("rules/", include("rules.urls", namespace="rules")),
    path("pick_cards/", include("pick_cards.urls", namespace="pick_cards")),
    path("evaluation/", include("evaluation.urls", namespace="evaluation")),
    path("ai_process/", include("ai_process.urls", namespace="ai_process")),
    path("conclusion/", include("conclusion.urls", namespace="conclusion")),
]
