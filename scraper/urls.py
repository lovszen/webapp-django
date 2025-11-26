from django.urls import path
from . import views

urlpatterns = [
    path('', views.buscar_alumnos, name='scraper_buscar'),
]