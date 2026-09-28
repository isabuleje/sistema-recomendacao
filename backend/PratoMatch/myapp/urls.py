from django.urls import path
from .views import (
    listar_pratos,
    listar_avaliados,
    categorias,
    ingredientes,
    pratos,
    salvar_onboarding,
    cadastrar_usuario,
)

urlpatterns = [
    path('pratos/', listar_pratos),
    path('avaliados/', listar_avaliados),
    path("categorias/", categorias),
    path("ingredientes/", ingredientes),
    path("pratos_data/", pratos),
    path(
        "api/onboarding/",
        salvar_onboarding,
        name="salvar_onboarding"
    ),
    path("cadastro/", cadastrar_usuario, name="cadastro"),

]