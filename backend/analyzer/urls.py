from django.urls import path
from .views import AnalyzeSEO

urlpatterns = [
    path("analyze/", AnalyzeSEO.as_view(), name="analyze_seo"),
]
