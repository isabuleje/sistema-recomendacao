from django.urls import path
from .views import listar_pratos, categorias, ingredientes, pratos


urlpatterns = [
    path('pratos/', listar_pratos),
    path("categorias/", categorias),
    path("ingredientes/", ingredientes),
    path("pratos_data/", pratos),
]