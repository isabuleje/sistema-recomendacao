"""
============================================================
SEED OFICIAL - PRATOMATCH
============================================================
Popula o banco com TODOS os dados do CSV (categorias, pratos,
usuários e interações) mais os catálogos fixos (alergias e
preferências alimentares).

Uso:
    python seed_oficial.py            -> popula o banco (não apaga nada)
    python seed_oficial.py --limpar   -> apaga os dados do seed e popula de novo

Observação: este script NÃO roda makemigrations. As migrations
são geradas pelo desenvolvedor (python manage.py makemigrations),
versionadas no Git e apenas aplicadas aqui com "migrate".
============================================================
"""

import os
import sys
import subprocess
from pathlib import Path

import pandas as pd
import ast

#O comando da maga
BASE_DIR = Path(__file__).resolve().parent
PRATOMATCH_DIR = BASE_DIR / "PratoMatch"

sys.path.insert(0, str(PRATOMATCH_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "configs.settings")


# ============================================================
# CONFIGURAÇÕES
# ============================================================
# None = sem limite (usa TUDO que existe no CSV)
LIMITE_USUARIOS = None
LIMITE_PRATOS = None
LIMITE_CATEGORIAS = None

# Cria respostas de onboarding a partir das primeiras interações
# de cada usuário. Isso é dado derivado, não vem direto do CSV.
CRIAR_ONBOARDING = True
ONBOARDING_POR_USUARIO = 8

# Senha dos usuários importados do CSV.
# None  -> senha inutilizável (ninguém consegue logar; recomendado
#          para produção, pois são usuários apenas de dados).
# "abc" -> todos ficam com essa senha (útil só em ambiente de teste).
SENHA_DEMO = None

# Prefixo do username dos usuários criados pelo seed.
PREFIXO_USERNAME = "usuario_"


# ============================================================
# MIGRAÇÕES
# ============================================================

def aplicar_migracoes():
    """Só aplica as migrations que já existem no projeto."""
    print("\nAplicando migrações...")

    subprocess.run(
        [sys.executable, "manage.py", "migrate"],
        cwd=PRATOMATCH_DIR,
        check=True,
    )


aplicar_migracoes()

import django

django.setup()

# Estes imports só funcionam depois do django.setup().
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db.models import Count

from myapp.models import (
    Categoria,
    Prato,
    Interacao,
    Alergia,
    PreferenciaAlimentar,
    PerfilUsuario,
    OnBoardingPrato,
    Ingrediente,
    IngredienteReceita
)

from recomendacao.main import (
    obter_categorias,
    obter_pratos,
    obter_pares_receita_ingrediente,
    INTERACOES,
)


# ============================================================
# LIMPEZA (só roda com --limpar, antes ia automaticamente mas como a gnt n ta mais mexendo no models ent n precisa)

def limpar_banco():
    """
    Apaga somente o que o seed cria.

    Usuários reais (cadastrados pelo app) NÃO são apagados:
    só removemos os usuários com o prefixo do seed.
    A ordem respeita as dependências entre as tabelas.
    """
    print("\nLimpando dados do seed...")

    OnBoardingPrato.objects.all().delete()
    Interacao.objects.all().delete()
    PerfilUsuario.objects.filter(
        usuario__username__startswith=PREFIXO_USERNAME
    ).delete()
    User.objects.filter(
        username__startswith=PREFIXO_USERNAME
    ).delete()
    Prato.objects.all().delete()
    Categoria.objects.all().delete()
    Alergia.objects.all().delete()
    PreferenciaAlimentar.objects.all().delete()

    print("Banco limpo!")


# ============================================================
# CATÁLOGOS FIXOS (não vêm do CSV)
# Tenho quase ctz que nao precisava dessa parte de criar categorias e alergias mas tudo bem, n faz mal n

def criar_categorias():
    """Cadastra as categorias encontradas no CSV."""
    print("\nCriando categorias...")

    # dict.fromkeys remove duplicadas mantendo a ordem.
    nomes = list(dict.fromkeys(obter_categorias()))

    if LIMITE_CATEGORIAS is not None:
        nomes = nomes[:LIMITE_CATEGORIAS]

    Categoria.objects.bulk_create(
        [Categoria(nome=nome) for nome in nomes],
        batch_size=1000,
        ignore_conflicts=True,  # rodar de novo não duplica
    )

    print(f"{Categoria.objects.count()} categorias no banco.")


def criar_alergias():
    print("\nCriando alergias...")

    nomes = ["Amendoim", "Leite", "Glúten", "Ovo", "Camarão", "Soja"]

    Alergia.objects.bulk_create(
        [Alergia(nome=nome) for nome in nomes],
        ignore_conflicts=True,
    )

    print(f"{Alergia.objects.count()} alergias no banco.")


def criar_preferencias():
    print("\nCriando preferências alimentares...")

    #Tirei o Onívoro e Low Carb pq onivoro é considerado nenhum e low carb nao tem como fazer pq n tem calorias nos pratos
    nomes = [
        "Vegetariano",
        "Vegano",
        "Sem Glúten",
        "Sem Lactose",
    ]

    PreferenciaAlimentar.objects.bulk_create(
        [PreferenciaAlimentar(nome=nome) for nome in nomes],
        ignore_conflicts=True,
    )

    print(f"{PreferenciaAlimentar.objects.count()} preferências no banco.")


# ============================================================
# PRATOS
# ============================================================

def criar_pratos():
    """
    Cadastra todos os pratos do CSV de receitas.
    Mantém o id original do CSV, assim as interações apontam
    direto para o prato certo.

    Retorna o conjunto de ids cadastrados.
    """
    print("\nCriando pratos...")

    pratos_csv = obter_pratos()

    if LIMITE_PRATOS is not None:
        pratos_csv = pratos_csv[:LIMITE_PRATOS]

    objetos = [
        Prato(id=int(dados["id"]), nome=dados["nome"])
        for dados in pratos_csv
        if dados["id"] is not None
    ]

    Prato.objects.bulk_create(
        objetos,
        batch_size=1000,
        ignore_conflicts=True,
    )

    print(f"{len(objetos)} pratos processados.")

    return {prato.id for prato in objetos}


# ============================================================
# INTERAÇÕES (limpeza do DataFrame)
# ============================================================

def preparar_interacoes(ids_pratos):
    """
    Limpa o DataFrame do CSV uma única vez:
      - remove linhas incompletas
      - mantém só notas de 1 a 5
      - mantém só receitas que existem na tabela Prato
      - deixa uma interação por usuário + prato (a mais recente)
      - aplica LIMITE_USUARIOS, se houver
    """
    print("\nPreparando interações do CSV...")

    df = INTERACOES[["user_id", "recipe_id", "rating", "date"]].dropna(
        subset=["user_id", "recipe_id", "rating"]
    ).copy()

    df["user_id"] = df["user_id"].astype(int)
    df["recipe_id"] = df["recipe_id"].astype(int)
    df["rating"] = df["rating"].astype(int)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    df = df[df["rating"].between(1, 5)]
    df = df[df["recipe_id"].isin(ids_pratos)]

    df = df.sort_values("date").drop_duplicates(
        subset=["user_id", "recipe_id"],
        keep="last",
    )

    if LIMITE_USUARIOS is not None:
        permitidos = df["user_id"].drop_duplicates().head(LIMITE_USUARIOS)
        df = df[df["user_id"].isin(permitidos)]

    print(
        f"{len(df)} interações válidas de "
        f"{df['user_id'].nunique()} usuários."
    )

    return df


# ============================================================
# USUÁRIOS E PERFIS
# ============================================================

def criar_usuarios(ids_usuarios):
    print("\nCriando usuários...")

    senha = make_password(SENHA_DEMO)

    # Sem id explícito: o banco escolhe o pk.
    objetos = [
        User(
            username=f"{PREFIXO_USERNAME}{uid}",
            email=f"usuario{uid}@pratomatch.com",
            password=senha,
        )
        for uid in ids_usuarios
    ]

    # Se o username já existe, o insert é ignorado e reaproveitamos
    # o usuário existente (o mapa abaixo pega os dois casos).
    User.objects.bulk_create(
        objetos,
        batch_size=1000,
        ignore_conflicts=True,
    )

    # Mapa {user_id do CSV: pk real do User}.
    tamanho = len(PREFIXO_USERNAME)
    mapa = {
        int(username[tamanho:]): pk
        for pk, username in User.objects
            .filter(username__startswith=PREFIXO_USERNAME)
            .values_list("id", "username")
        if username[tamanho:].isdigit()
    }

    print(f"{len(mapa)} usuários prontos.")
    return mapa

def criar_perfis(mapa_usuarios):
    """
    Cria um PerfilUsuario vazio para cada usuário do seed.

    Alergias, preferências e categorias preferidas ficam vazias de
    propósito: o CSV não tem essa informação, e inventar valores
    para usuários "oficiais" poderia distorcer as recomendações.
    
    Realmente n tem motivo real pra popular esses perfils, antes era so pra vc ver como ficava
    """
    print("\nCriando perfis...")

    PerfilUsuario.objects.bulk_create(
        [PerfilUsuario(usuario_id=pk) for pk in mapa_usuarios.values()],
        batch_size=1000,
        ignore_conflicts=True,
    )

    print(f"{PerfilUsuario.objects.count()} perfis no banco.")


# ============================================================
# INTERAÇÕES (gravação no banco)
# ============================================================

def criar_interacoes(df):
    print("\nCriando interações...")

    if Interacao.objects.exists():
        print("Já existem interações; pulando (use --limpar para refazer).")
        return

    objetos = []

    # itertuples é bem mais rápido que iterrows para muitas linhas
    # aparentemente iterrows é horrivel pq eu usei ele no main e demorou seculos pra rodar tudo
    for linha in df.itertuples(index=False):
        campos = {}

        # Obs.: se o campo "data" do model for auto_now_add, o Django
        # ignora este valor e grava a data do momento do seed.
        if not pd.isna(linha.date):
            campos["data"] = linha.date

        objetos.append(
            Interacao(
                usuario_id=linha.usuario_pk,
                prato_id=linha.recipe_id,
                nota=linha.rating,
                interesse=linha.rating >= 4,
                # Confira se estes valores batem com as choices do model.
                status="favorito" if linha.rating == 5 else "visualizado",
                **campos,
            )
        )

    Interacao.objects.bulk_create(
        objetos,
        batch_size=2000,
        ignore_conflicts=True,
    )

    print(f"{len(objetos)} interações criadas.")


# ============================================================
# ONBOARDING
# ============================================================

def criar_onboarding(df):
    """
    Para cada usuário, usa as primeiras interações (por id do prato)
    como se fossem as respostas do onboarding.
    """
    print("\nCriando dados de onboarding...")

    if OnBoardingPrato.objects.exists():
        print("Já existe onboarding; pulando (use --limpar para refazer).")
        return

    # {usuario_id: perfil_id}, uma única consulta.
    perfil_por_usuario = dict(
        PerfilUsuario.objects.values_list("usuario_id", "id")
    )

    amostra = (
        df.sort_values(["user_id", "recipe_id"])
        .groupby("user_id")
        .head(ONBOARDING_POR_USUARIO)
    )

    objetos = [
        OnBoardingPrato(
            perfil_id=perfil_por_usuario[linha.usuario_pk],
            prato_id=linha.recipe_id,
            interesse=linha.rating >= 4,
        )
        for linha in amostra.itertuples(index=False)
        if linha.usuario_pk in perfil_por_usuario
    ]

    OnBoardingPrato.objects.bulk_create(
        objetos,
        batch_size=2000,
        ignore_conflicts=True,  # respeita a UniqueConstraint
    )

    print(f"{len(objetos)} respostas de onboarding criadas.")

#ingredientes oi

from recomendacao.main import obter_pares_receita_ingrediente

def criar_ingredientes(ids_pratos):
    print("\nCriando ingredientes e associações...")

    pares = obter_pares_receita_ingrediente(ids_pratos)
    ids_ingredientes = {ing_id for _, ing_id in pares}

    Ingrediente.objects.bulk_create(
        [Ingrediente(id=i, nome=f"ingrediente_{i}") for i in ids_ingredientes],
        batch_size=5000,
        ignore_conflicts=True,
    )

    IngredienteReceita.objects.bulk_create(
        [IngredienteReceita(prato_id=p, ingrediente_id=i) for p, i in pares],
        batch_size=5000,
        ignore_conflicts=True,
    )

    print(f"{len(ids_ingredientes)} ingredientes e {len(pares)} associações criadas.")

# ============================================================
# EXECUÇÃO
# ============================================================

def main():
    print("\n" + "=" * 60)
    print("        POPULANDO BANCO - PRATOMATCH")
    print("=" * 60)

    if "--limpar" in sys.argv:
        limpar_banco()

    # 1) Catálogos
    criar_categorias()
    criar_alergias()
    criar_preferencias()

    # 2) Pratos (precisam existir antes das interações)
    ids_pratos = criar_pratos()

    # 3) Interações do CSV, já filtradas e limpas
    df = preparar_interacoes(ids_pratos)
    ids_usuarios = df["user_id"].drop_duplicates().tolist()

    mapa = criar_usuarios(ids_usuarios)

    # Traduz o id do CSV para o pk real do User.
    df = df[df["user_id"].isin(mapa)].copy()
    df["usuario_pk"] = df["user_id"].map(mapa)

    criar_perfis(mapa)
    criar_interacoes(df)
    criar_ingredientes(ids_pratos)


    if CRIAR_ONBOARDING:
        criar_onboarding(df)

    print("\n" + "=" * 60)
    print("        BANCO POPULADO COM SUCESSO!")
    print("=" * 60)

    print("\nResumo:")
    print(f"Usuários: {User.objects.count()}")
    print(f"Perfis: {PerfilUsuario.objects.count()}")
    print(f"Pratos: {Prato.objects.count()}")
    print(f"Categorias: {Categoria.objects.count()}")
    print(f"Alergias: {Alergia.objects.count()}")
    print(f"Preferências: {PreferenciaAlimentar.objects.count()}")
    print(f"Interações: {Interacao.objects.count()}")
    print(f"Onboarding: {OnBoardingPrato.objects.count()}")
    print(f"Ingredientes: {Ingrediente.objects.count()}")

    print("\nPratos mais avaliados:")

    top = (
        Interacao.objects
        .values("prato__nome")
        .annotate(qtd=Count("usuario"))
        .order_by("-qtd")[:10]
    )

    for item in top:
        print(f"  {item['prato__nome']} -> {item['qtd']} usuários")


if __name__ == "__main__":
    main()