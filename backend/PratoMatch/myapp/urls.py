from django.urls import path
from .views import (
    listar_pratos,
    listar_avaliados,
    salvar_avaliacao,
    categorias,
    ingredientes,
    pratos,
    salvar_onboarding,
    cadastrar_usuario,
    entrar_usuario,
    csrf_token,
    pesquisar_pratos,
    listar_favoritos,
    salvar_favoritos,
    recomendados
)

#fico imaginando como deve ser em projetos enormes, como q eles organizam esses paths
urlpatterns = [
    path("csrf/", csrf_token, name="csrf_token"),
    path('pratos/', listar_pratos),
    path('avaliados/', listar_avaliados),
    path('avaliacoes/', salvar_avaliacao),
    path("categorias/", categorias),
    path("ingredientes/", ingredientes),
    path("pratos_data/", pratos),
    path("onboarding/", salvar_onboarding, name="salvar_onboarding"),
    path("cadastro/", cadastrar_usuario, name="cadastro"),
    path("login/", entrar_usuario, name="login"),
    path('pesquisar/', pesquisar_pratos),
    path("favoritos/", listar_favoritos),
    path("favoritos/salvar/", salvar_favoritos),
    path("recomendados/", recomendados),
]