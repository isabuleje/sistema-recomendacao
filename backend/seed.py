import os
import sys
import subprocess
from pathlib import Path

'''#
dps a gnt nao pode esquecer de tirar isso daq do codigo kkkkkkkkkkkkk
meu grande mano gepete dando uma ajuda pra gnt, valeu mano
'''
BASE_DIR = Path(__file__).resolve().parent
PRATOMATCH_DIR = BASE_DIR / "PratoMatch"

sys.path.insert(0, str(PRATOMATCH_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "configs.settings")

# ============================================================
# DJANGO: MIGRAÇÕES AUTOMÁTICAS
# ============================================================
# Assim você não precisa ficar executando os comandos manualmente
# sempre que alterar os models.
#
# Equivale a:
#   python manage.py makemigrations
#   python manage.py migrate
# ============================================================

def preparar_banco():
    print("\nVerificando alterações nos models...")

    subprocess.run(
        [sys.executable, "manage.py", "makemigrations"],
        cwd=PRATOMATCH_DIR,
        check=True,
    )

    print("\nAplicando migrações...")
    subprocess.run(
        [sys.executable, "manage.py", "migrate"],
        cwd=PRATOMATCH_DIR,
        check=True,
    )

    print("\nBanco pronto!")


preparar_banco()

import django

django.setup()

# ============================================================
# MODELS
# ============================================================

from django.contrib.auth.models import User
from django.db.models import Count
from myapp.models import (
    Categoria,
    Prato,
    Interacao,
    Alergia,
    PreferenciaAlimentar,
    PerfilUsuario,
)

from recomendacao.main import (
    obter_categorias,
    obter_pratos,
    INTERACOES,
)

# ============================================================
# CONFIGURAÇÕES DO SEED
# ============================================================

LIMITE_USUARIOS = 10

USUARIOS_CANDIDATOS = 100

LIMITE_PRATOS = None

LIMITE_CATEGORIAS = 10
# ============================================================
# LIMPAR DADOS GERADOS PELO SEED
# ============================================================

def limpar_banco():
    print("\nLimpando dados antigos...")

    Interacao.objects.all().delete()
    PerfilUsuario.objects.all().delete()
    Prato.objects.all().delete()
    Categoria.objects.all().delete()
    Alergia.objects.all().delete()
    PreferenciaAlimentar.objects.all().delete()

    print("Banco limpo!")


# ============================================================
# ESCOLHER USUÁRIOS COM RECEITAS EM COMUM
# ============================================================
# ============================================================
# ESCOLHER POUCOS USUÁRIOS COM RECEITAS EM COMUM
# ============================================================

def selecionar_usuarios_comuns():

    print("\nProcurando poucos usuários com receitas em comum...")

    # --------------------------------------------------------
    # PEGAMOS SOMENTE UMA PEQUENA PARTE DOS USUÁRIOS
    # --------------------------------------------------------

    usuarios_disponiveis = (
        INTERACOES["user_id"]
        .dropna()
        .astype(int)
        .drop_duplicates()
        .tolist()
    )

    candidatos_ids = usuarios_disponiveis[:USUARIOS_CANDIDATOS]

    print(
        f"Analisando somente {len(candidatos_ids)} "
        f"usuários candidatos..."
    )

    # --------------------------------------------------------
    # FILTRA O DATAFRAME
    # --------------------------------------------------------

    dados = INTERACOES[
        INTERACOES["user_id"].isin(candidatos_ids)
    ][
        ["user_id", "recipe_id"]
    ].dropna()

    dados["user_id"] = dados["user_id"].astype(int)
    dados["recipe_id"] = dados["recipe_id"].astype(int)

    # --------------------------------------------------------
    # RECEITAS DE CADA USUÁRIO
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # PROCURA UM GRUPO PEQUENO
    # --------------------------------------------------------

    for referencia in usuarios:

        receitas_referencia = receitas_por_usuario[referencia]

        selecionados = [referencia]

        for usuario_id in usuarios:

            if usuario_id == referencia:
                continue

            receitas_usuario = receitas_por_usuario[usuario_id]

            comuns = receitas_referencia & receitas_usuario

            if comuns:

                selecionados.append(usuario_id)

                print(
                    f"Usuário {usuario_id}: "
                    f"{len(comuns)} receitas em comum"
                )

            # Já temos usuários suficientes
            if len(selecionados) >= LIMITE_USUARIOS:
                break

        if len(selecionados) >= LIMITE_USUARIOS:

            print(
                f"\nGrupo encontrado!"
            )

            print(
                f"Usuário de referência: {referencia}"
            )

            print(
                f"Usuários selecionados: "
                f"{len(selecionados)}"
            )

            return selecionados

    # --------------------------------------------------------
    # CASO NÃO ENCONTRE
    # --------------------------------------------------------

    raise RuntimeError(
        "Não foram encontrados usuários suficientes "
        "com receitas em comum dentro dos candidatos."
    )

# ============================================================
# CRIAR CATEGORIAS
# ============================================================

def criar_categorias():
    """
    Não cadastra todas as categorias do CSV.

    Apenas algumas categorias são necessárias para montar os
    perfis de teste.
    """

    print("\nCriando categorias de exemplo...")

    categorias_csv = obter_categorias()

    # Mantém somente uma pequena quantidade.
    categorias = list(categorias_csv)[:LIMITE_CATEGORIAS]

    categorias_obj = {}

    for nome in categorias:
        categoria, _ = Categoria.objects.get_or_create(nome=nome)
        categorias_obj[nome] = categoria

    print(f"{len(categorias_obj)} categorias criadas.")

    return categorias_obj


# ============================================================
# CRIAR PRATOS
# ============================================================

def criar_pratos(usuarios_ids):
    print("\nCriando pratos dos usuários selecionados...")

    user_ids = set(usuarios_ids)

    # Apenas interações dos usuários escolhidos.
    interacoes = INTERACOES[
        INTERACOES["user_id"].isin(user_ids)
    ].copy()

    interacoes["recipe_id"] = interacoes["recipe_id"].astype(int)

    # Mantemos somente receitas avaliadas por pelo menos 2 dos
    # usuários selecionados. Assim o banco fica menor e os usuários
    # realmente possuem receitas em comum.
    ids_pratos = (
        interacoes.groupby("recipe_id")["user_id"]
        .nunique()
    )
    ids_pratos = ids_pratos[ids_pratos >= 2].index

    if LIMITE_PRATOS is not None:
        ids_pratos = ids_pratos[:LIMITE_PRATOS]

    ids_pratos = set(int(id_prato) for id_prato in ids_pratos)

    print(
        f"Encontrados {len(ids_pratos)} pratos compartilhados "
        f"por pelo menos 2 usuários."
    )

    # O CSV de receitas é lido uma vez.
    pratos_dados = obter_pratos()

    pratos_dados = [
        prato
        for prato in pratos_dados
        if prato["id"] in ids_pratos
    ]

    # Como o banco foi limpo, bulk_create é muito mais rápido
    # do que fazer update_or_create para cada receita.
    pratos_obj = []

    for dados in pratos_dados:
        if dados["id"] is None:
            continue

        pratos_obj.append(
            Prato(
                id=int(dados["id"]),
                nome=dados["nome"],
            )
        )

    if pratos_obj:
        Prato.objects.bulk_create(
            pratos_obj,
            batch_size=1000,
            ignore_conflicts=True,
        )

    pratos_obj = {
        prato.id: prato
        for prato in Prato.objects.filter(
            id__in=ids_pratos
        )
    }

    print(f"{len(pratos_obj)} pratos cadastrados.")

    return pratos_obj


# ============================================================
# CRIAR ALERGIAS
# ============================================================

def criar_alergias():
    print("\nCriando alergias...")

    nomes = [
        "Amendoim",
        "Leite",
        "Glúten",
        "Ovo",
        "Camarão",
        "Soja",
    ]

    alergias = {}

    objetos = [
        Alergia(nome=nome)
        for nome in nomes
    ]

    Alergia.objects.bulk_create(
        objetos,
        ignore_conflicts=True,
    )

    for alergia in Alergia.objects.filter(nome__in=nomes):
        alergias[alergia.nome] = alergia

    print(f"{len(alergias)} alergias criadas.")

    return alergias


# ============================================================
# CRIAR PREFERÊNCIAS ALIMENTARES
# ============================================================

def criar_preferencias():
    print("\nCriando preferências alimentares...")

    nomes = [
        "Vegetariano",
        "Vegano",
        "Onívoro",
        "Low Carb",
        "Sem Glúten",
        "Sem Lactose",
    ]

    objetos = [
        PreferenciaAlimentar(nome=nome)
        for nome in nomes
    ]

    PreferenciaAlimentar.objects.bulk_create(
        objetos,
        ignore_conflicts=True,
    )

    preferencias = {
        preferencia.nome: preferencia
        for preferencia in PreferenciaAlimentar.objects.filter(
            nome__in=nomes
        )
    }

    print(f"{len(preferencias)} preferências criadas.")

    return preferencias


# ============================================================
# CRIAR USUÁRIOS
# ============================================================

def criar_usuarios(usuarios_ids):
    print("\nCriando usuários de demonstração...")

    usuarios = {}

    for numero in usuarios_ids:
        numero = int(numero)
        username = f"usuario_{numero}"

        usuario, created = User.objects.get_or_create(
            username=username,
            defaults={
                "email": f"usuario{numero}@pratomatch.com"
            },
        )

        if created:
            usuario.set_password("123456")
            usuario.save()

        usuarios[numero] = usuario

    print(f"{len(usuarios)} usuários preparados.")

    return usuarios


# ============================================================
# CRIAR PERFIS
# ============================================================

def criar_perfis(
    usuarios,
    alergias,
    preferencias,
    categorias,
):
    print("\nCriando perfis dos usuários...")

    preferencias_lista = list(preferencias.values())
    alergias_lista = list(alergias.values())
    categorias_lista = list(categorias.values())

    perfis = []

    for usuario in usuarios.values():
        perfil = PerfilUsuario(usuario=usuario)
        perfis.append(perfil)

    # Como os perfis acabaram de ser apagados, podemos inserir em lote.
    PerfilUsuario.objects.bulk_create(
        perfis,
        batch_size=100,
    )

    # Precisamos buscar os objetos criados para os relacionamentos M2M.
    perfis = list(
        PerfilUsuario.objects.filter(
            usuario__in=usuarios.values()
        )
    )

    for contador, perfil in enumerate(perfis):
        # Preferência
        if preferencias_lista:
            perfil.preferencias.add(
                preferencias_lista[contador % len(preferencias_lista)]
            )

        # Alergia
        if alergias_lista and contador % 2 == 0:
            perfil.alergias.add(
                alergias_lista[contador % len(alergias_lista)]
            )

        # Categoria: somente entre as poucas categorias cadastradas.
        if categorias_lista:
            perfil.categorias_preferidas.add(
                categorias_lista[contador % len(categorias_lista)]
            )

    print(f"{len(perfis)} perfis configurados.")


# ============================================================
# CRIAR INTERAÇÕES
# ============================================================

def criar_interacoes(
    usuarios,
    pratos,
):
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

    # Uma interação por usuário + prato.
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

        if __import__("pandas").isna(data):
            data = None

        objetos.append(
            Interacao(
                usuario=usuarios[user_id],
                prato=pratos[recipe_id],
                nota=rating,
                interesse=rating >= 4,
                status="favorito" if rating == 5 else "visualizado",
                **({"data": data} if data is not None else {}),
            )
        )

    if objetos:
        Interacao.objects.bulk_create(
            objetos,
            batch_size=1000,
            ignore_conflicts=True,
        )

    print(f"{len(objetos)} interações criadas.")


# ============================================================
# EXECUÇÃO
# ============================================================

def main():
    print("\n" + "=" * 60)
    print("        POPULANDO BANCO - PRATOMATCH")
    print("=" * 60)

    limpar_banco()

    # Primeiro escolhemos usuários que realmente possuem
    # receitas em comum.
    usuarios_ids = selecionar_usuarios_comuns()

    categorias = criar_categorias()
    alergias = criar_alergias()
    preferencias = criar_preferencias()

    usuarios = criar_usuarios(usuarios_ids)

    pratos = criar_pratos(usuarios_ids)

    criar_perfis(
        usuarios,
        alergias,
        preferencias,
        categorias,
    )

    criar_interacoes(
        usuarios,
        pratos,
    )

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

    print("\nUsuários de teste:")

    for usuario in usuarios.values():
        print(
            f"  {usuario.username} "
            f"(senha: 123456)"
        )

    print("\nReceitas compartilhadas:")

    # Mostra apenas algumas receitas que aparecem para mais
    # de um usuário, sem imprimir milhares de linhas.
    comuns = (
        Interacao.objects
        .values("prato")
        .annotate(qtd=Count("usuario"))
        .filter(qtd__gt=1)
        .order_by("-qtd")[:10]
    )

    for item in comuns:
        prato = Prato.objects.get(id=item["prato"])
        print(
            f"  {prato.nome} -> "
            f"{item['qtd']} usuários"
        )


if __name__ == "__main__":
    main()
