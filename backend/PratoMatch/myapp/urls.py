from django.urls import path
from .views import listar_pratos, categorias, ingredientes, pratos, salvar_onboarding


urlpatterns = [
    path('pratos/', listar_pratos),
    path("categorias/", categorias),
    path("ingredientes/", ingredientes),
    path("pratos_data/", pratos),
    path(
        "api/onboarding/",
        salvar_onboarding,
        name="salvar_onboarding"
    ),
]