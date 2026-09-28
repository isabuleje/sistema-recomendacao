import os
import sys
from pathlib import Path

# ============================================================
# CONFIGURAÇÃO DO DJANGO
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
PRATOMATCH_DIR = BASE_DIR / "PratoMatch"

sys.path.insert(0, str(PRATOMATCH_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "configs.settings")

import django

django.setup()

from django.contrib.auth.models import User
from django.db.models import Count

from myapp.models import Prato, Interacao
from recomendacao.main import INTERACOES, obter_pratos


# ============================================================
# CONFIGURAÇÕES
# ============================================================

LIMITE_USUARIOS = 10
USUARIOS_CANDIDATOS = 100


# ============================================================
# LIMPAR SOMENTE O QUE ESTE TESTE USA
# ============================================================

def limpar_banco():
    print("\nLimpando dados antigos...")

    Interacao.objects.all().delete()
    Prato.objects.all().delete()

    # Remove os usuários criados por este script.
    User.objects.filter(username__startswith="usuario_").delete()

    print("Banco limpo!")


# ============================================================
# ESCOLHER USUÁRIOS QUE POSSUEM RECEITAS EM COMUM
# ============================================================

def selecionar_usuarios_comuns():
    print("\nProcurando usuários com receitas em comum...")

    usuarios_disponiveis = (
        INTERACOES["user_id"]
        .dropna()
        .astype(int)
        .drop_duplicates()
        .tolist()
    )

    candidatos_ids = usuarios_disponiveis[:USUARIOS_CANDIDATOS]

    dados = INTERACOES[
        INTERACOES["user_id"].isin(candidatos_ids)
    ][["user_id", "recipe_id"]].dropna()

    dados["user_id"] = dados["user_id"].astype(int)
    dados["recipe_id"] = dados["recipe_id"].astype(int)

    receitas_por_usuario = (
        dados.groupby("user_id")["recipe_id"]
        .agg(set)
        .to_dict()
    )

    usuarios = list(receitas_por_usuario.keys())

    if len(usuarios) < 2:
        raise RuntimeError(
            "Não existem usuários suficientes para o teste."
        )

    for referencia in usuarios:
        receitas_referencia = receitas_por_usuario[referencia]
        selecionados = [referencia]

        for usuario_id in usuarios:
            if usuario_id == referencia:
                continue

            comuns = (
                receitas_referencia
                & receitas_por_usuario[usuario_id]
            )

            if comuns:
                selecionados.append(usuario_id)

            if len(selecionados) >= LIMITE_USUARIOS:
                break

        if len(selecionados) >= LIMITE_USUARIOS:
            print(f"Usuário de referência: {referencia}")
            print(f"Usuários selecionados: {len(selecionados)}")
            return selecionados

    raise RuntimeError(
        "Não foram encontrados usuários suficientes "
        "com receitas em comum."
    )


# ============================================================
# CRIAR USUÁRIOS
# ============================================================

def criar_usuarios(usuarios_ids):
    print("\nCriando usuários de teste...")

    usuarios = {}

    for numero in usuarios_ids:
        numero = int(numero)
        username = f"usuario_{numero}"

        usuario = User.objects.create_user(
            username=username,
            email=f"usuario{numero}@pratomatch.com",
            password="123456",
        )

        usuarios[numero] = usuario

    print(f"{len(usuarios)} usuários criados.")

    return usuarios


# ============================================================
# CRIAR PRATOS
# ============================================================

def criar_pratos(usuarios_ids):
    print("\nCriando pratos compartilhados...")

    user_ids = set(usuarios_ids)

    interacoes = INTERACOES[
        INTERACOES["user_id"].isin(user_ids)
    ].copy()

    interacoes["recipe_id"] = interacoes["recipe_id"].astype(int)

    # Só entram receitas avaliadas por pelo menos 2
    # dos usuários selecionados.
    ids_pratos = (
        interacoes.groupby("recipe_id")["user_id"]
        .nunique()
    )

    ids_pratos = set(
        int(recipe_id)
        for recipe_id in ids_pratos[ids_pratos >= 2].index
    )

    pratos_dados = obter_pratos()

    pratos_obj = [
        Prato(
            id=int(prato["id"]),
            nome=prato["nome"],
        )
        for prato in pratos_dados
        if prato["id"] in ids_pratos
    ]

    if pratos_obj:
        Prato.objects.bulk_create(
            pratos_obj,
            batch_size=1000,
            ignore_conflicts=True,
        )

    pratos = {
        prato.id: prato
        for prato in Prato.objects.filter(id__in=ids_pratos)
    }

    print(f"{len(pratos)} pratos cadastrados.")

    return pratos


# ============================================================
# CRIAR INTERAÇÕES
# ============================================================

def criar_interacoes(usuarios, pratos):
    print("\nCriando interações...")

    user_ids = list(usuarios.keys())

    interacoes = INTERACOES[
        INTERACOES["user_id"].isin(user_ids)
    ].copy()

    interacoes["date"] = __import__("pandas").to_datetime(
        interacoes["date"],
        errors="coerce",
    )

    interacoes = interacoes[
        interacoes["rating"].between(1, 5)
    ].copy()

    # Uma avaliação por usuário + prato.
    interacoes = (
        interacoes
        .sort_values("date")
        .drop_duplicates(
            subset=["user_id", "recipe_id"],
            keep="last",
        )
    )

    objetos = []

    for _, linha in interacoes.iterrows():
        user_id = int(linha["user_id"])
        recipe_id = int(linha["recipe_id"])
        rating = int(linha["rating"])

        if user_id not in usuarios:
            continue

        if recipe_id not in pratos:
            continue

        data = linha["date"]

        kwargs = {
            "usuario": usuarios[user_id],
            "prato": pratos[recipe_id],
            "nota": rating,
            "interesse": rating >= 4,
            "status": "favorito" if rating == 5 else "visualizado",
        }

        if not __import__("pandas").isna(data):
            kwargs["data"] = data

        objetos.append(Interacao(**kwargs))

    if objetos:
        Interacao.objects.bulk_create(
            objetos,
            batch_size=1000,
            ignore_conflicts=True,
        )

    print(f"{len(objetos)} interações criadas.")


# ============================================================
# MOSTRAR RESULTADO DO TESTE
# ============================================================

def mostrar_receitas_compartilhadas():
    print("\n" + "=" * 70)
    print("RECEITAS COMPARTILHADAS")
    print("=" * 70)

    # Count DISTINCT garante que a quantidade representa
    # o número real de usuários que avaliaram cada prato.
    comuns = (
        Interacao.objects
        .values("prato")
        .annotate(
            total_avaliadores=Count(
                "usuario",
                distinct=True,
            )
        )
        .filter(total_avaliadores__gt=1)
        .order_by("-total_avaliadores")[:10]
    )

    for item in comuns:
        prato = Prato.objects.get(id=item["prato"])

        usuarios_ids = list(
            Interacao.objects
            .filter(prato_id=prato.id)
            .values_list("usuario_id", flat=True)
            .distinct()
        )

        print(
            f"\n{prato.nome}"
            f"\n  Total de avaliadores: {len(usuarios_ids)}"
            f"\n  IDs dos avaliadores: {usuarios_ids}"
        )


# ============================================================
# EXECUÇÃO
# ============================================================

def main():
    print("\n" + "=" * 70)
    print("POPULANDO BANCO PARA TESTE DE RECOMENDAÇÃO")
    print("=" * 70)

    limpar_banco()

    usuarios_ids = selecionar_usuarios_comuns()

    usuarios = criar_usuarios(usuarios_ids)

    pratos = criar_pratos(usuarios_ids)

    criar_interacoes(
        usuarios,
        pratos,
    )

    mostrar_receitas_compartilhadas()

    print("\n" + "=" * 70)
    print("BANCO POPULADO COM SUCESSO!")
    print("=" * 70)


if __name__ == "__main__":
    main()
