from django.urls import path
from .views import listar_pratos, categorias, ingredientes


urlpatterns = [
    path('pratos/', listar_pratos),
    path("categorias/", categorias),
    path("ingredientes/", ingredientes),
]