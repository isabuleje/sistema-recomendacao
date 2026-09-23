from django.urls import path
from .views import listar_pratos


urlpatterns = [
    path('pratos/', listar_pratos),
]