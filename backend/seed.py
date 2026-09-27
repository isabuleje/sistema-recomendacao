import os
import sys
from pathlib import Path


#Configurações de diretório porque o seed.py n ta dentro do Django em si
BASE_DIR = Path(__file__).resolve().parent

PRATOMATCH_DIR = BASE_DIR / "PratoMatch"

sys.path.insert(0, str(PRATOMATCH_DIR))

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "configs.settings"
)

import django

django.setup()


#modelos dentro do django
from django.contrib.auth.models import User
from myapp.models import (
    Categoria,
    Prato,
    Interacao,
    Alergia,
    PreferenciaAlimentar,
    PerfilUsuario,
)


#já tá pegando de dentro do sistema de recomendação
from recomendacao.main import (
    obter_categorias,
    obter_pratos,
    INTERACOES,
)


#dá pra ajustar mas n precisa
LIMITE_PRATOS = None

#10 só pra teste
LIMITE_USUARIOS = 10


#Aq meu mano gepete fez já que é só pra teste
def limpar_banco():

    print("\nLimpando dados antigos...")

    Interacao.objects.all().delete()
    PerfilUsuario.objects.all().delete()

    # Não apagamos o User inteiro porque ele pode
    # estar sendo usado pelo sistema de login.

    Prato.objects.all().delete()
    Categoria.objects.all().delete()

    Alergia.objects.all().delete()
    PreferenciaAlimentar.objects.all().delete()

    print("Banco limpo!")


# ============================================================
# CRIAR CATEGORIAS
# ============================================================

def criar_categorias():

    print("\nCriando categorias...")

    categorias = obter_categorias()

    categorias_obj = {}

    for nome in categorias:

        categoria, _ = Categoria.objects.get_or_create(
            nome=nome
        )

        categorias_obj[nome] = categoria

    print(
        f"{len(categorias_obj)} categorias criadas."
    )

    return categorias_obj




# ============================================================
# CRIAR PRATOS
# ============================================================

def criar_pratos(usuarios):
    print("\nCriando somente os pratos dos usuários selecionados...")

    # IDs dos usuários que realmente serão cadastrados
    user_ids = list(usuarios.keys())

    # Pega somente as interações desses usuários
    interacoes = INTERACOES[
        INTERACOES["user_id"].isin(user_ids)
    ].copy()

    # IDs dos pratos avaliados por esses usuários
    ids_pratos = (
        interacoes["recipe_id"]
        .dropna()
        .astype(int)
        .unique()
    )

    print(
        f"Encontrados {len(ids_pratos)} pratos "
        f"avaliados pelos {len(user_ids)} usuários."
    )

    # Busca os dados dos pratos no CSV
    pratos_dados = obter_pratos()

    # Mantém somente os pratos que esses usuários avaliaram
    pratos_dados = [
        prato
        for prato in pratos_dados
        if prato["id"] in ids_pratos
    ]

    pratos_obj = {}

    for dados in pratos_dados:

        if dados["id"] is None:
            continue

        prato, _ = Prato.objects.update_or_create(
            id=dados["id"],
            defaults={
                "nome": dados["nome"]
            }
        )

        pratos_obj[prato.id] = prato

    print(
        f"{len(pratos_obj)} pratos cadastrados no banco."
    )

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

    for nome in nomes:

        alergia, _ = Alergia.objects.get_or_create(
            nome=nome
        )

        alergias[nome] = alergia

    print(
        f"{len(alergias)} alergias criadas."
    )

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

    preferencias = {}

    for nome in nomes:

        preferencia, _ = PreferenciaAlimentar.objects.get_or_create(
            nome=nome
        )

        preferencias[nome] = preferencia

    print(
        f"{len(preferencias)} preferências criadas."
    )

    return preferencias


# ============================================================
# CRIAR USUÁRIOS
# ============================================================

def criar_usuarios():

    print("\nCriando usuários de demonstração...")

    # Pegamos somente usuários que realmente aparecem
    # no arquivo RAW_interactions.csv

    usuarios_csv = (
        INTERACOES["user_id"]
        .dropna()
        .drop_duplicates()
        .tolist()
    )

    usuarios_csv = usuarios_csv[:LIMITE_USUARIOS]

    usuarios = {}

    for numero in usuarios_csv:

        numero = int(numero)

        #Acho q era isso aq vc queria saber, os IDs estao sendo criados com base com oq ta no CSV, mas e mudavel
        username = f"usuario_{numero}"

        usuario, created = User.objects.get_or_create(
            username=username,
            defaults={
                "email": f"usuario{numero}@pratomatch.com"
            }
        )

        # Senha para poder testar o login
        if created:
            usuario.set_password("123456")
            usuario.save()

        usuarios[numero] = usuario

    print(
        f"{len(usuarios)} usuários criados."
    )

    return usuarios


# ============================================================
# CRIAR PERFIS
# ============================================================

def criar_perfis(
    usuarios,
    alergias,
    preferencias,
    categorias
):

    print("\nCriando perfis dos usuários...")

    preferencias_lista = list(
        preferencias.values()
    )

    alergias_lista = list(
        alergias.values()
    )

    categorias_lista = list(
        categorias.values()
    )

    for contador, usuario in enumerate(
        usuarios.values()
    ):

        perfil, _ = PerfilUsuario.objects.get_or_create(
            usuario=usuario
        )

        # ----------------------------------------------------
        # Preferências
        # ----------------------------------------------------

        if preferencias_lista:

            if contador % 3 == 0:

                perfil.preferencias.add(
                    preferencias_lista[0]
                )

            elif contador % 3 == 1:

                perfil.preferencias.add(
                    preferencias_lista[1]
                )

            else:

                perfil.preferencias.add(
                    preferencias_lista[2]
                )

        # ----------------------------------------------------
        # Alergias
        # ----------------------------------------------------

        if alergias_lista:

            # Alguns usuários terão alergias
            if contador % 2 == 0:

                perfil.alergias.add(
                    alergias_lista[
                        contador % len(alergias_lista)
                    ]
                )

        # ----------------------------------------------------
        # Categorias preferidas
        # ----------------------------------------------------

        if categorias_lista:

            # Cada usuário recebe até 2 categorias
            indice = contador % len(categorias_lista)

            perfil.categorias_preferidas.add(
                categorias_lista[indice]
            )

            if len(categorias_lista) > 1:

                segundo_indice = (
                    indice + 1
                ) % len(categorias_lista)

                perfil.categorias_preferidas.add(
                    categorias_lista[
                        segundo_indice
                    ]
                )

    print(
        f"{len(usuarios)} perfis configurados."
    )


# ============================================================
# CRIAR INTERAÇÕES
# ============================================================

def criar_interacoes(
    usuarios,
    pratos
):

    print("\nCriando interações...")

    # --------------------------------------------------------
    # Filtrar somente os usuários que criamos
    # --------------------------------------------------------

    user_ids = list(
        usuarios.keys()
    )

    interacoes = INTERACOES[
        INTERACOES["user_id"].isin(user_ids)
    ].copy()

    # --------------------------------------------------------
    # Converter datas
    # --------------------------------------------------------

    interacoes["date"] = (
        __import__("pandas")
        .to_datetime(
            interacoes["date"],
            errors="coerce"
        )
    )

    # --------------------------------------------------------
    # Somente notas válidas de 1 a 5
    # --------------------------------------------------------

    interacoes = interacoes[
        interacoes["rating"].between(1, 5)
    ]

    # --------------------------------------------------------
    # Seu model permite apenas uma interação
    # por usuário + prato.
    #
    # Então, se o CSV tiver várias interações
    # para a mesma combinação, pegamos a mais recente.
    # --------------------------------------------------------

    interacoes = (
        interacoes
        .sort_values("date")
        .drop_duplicates(
            subset=[
                "user_id",
                "recipe_id"
            ],
            keep="last"
        )
    )

    quantidade = 0

    for _, linha in interacoes.iterrows():

        user_id = int(
            linha["user_id"]
        )

        recipe_id = int(
            linha["recipe_id"]
        )

        rating = int(
            linha["rating"]
        )

        # Verifica se o usuário existe
        if user_id not in usuarios:
            continue

        # Verifica se o prato existe
        if recipe_id not in pratos:
            continue

        usuario = usuarios[user_id]

        prato = pratos[recipe_id]

        # Interesse baseado na nota
        interesse = rating >= 4

        # Status baseado na nota
        if rating == 5:

            status = "favorito"

        else:

            status = "visualizado"

        # Data
        data = linha["date"]

        if __import__("pandas").isna(data):
            data = None

        # ----------------------------------------------------
        # Como existe UniqueConstraint(usuario, prato),
        # usamos update_or_create.
        # ----------------------------------------------------

        interacao, created = Interacao.objects.update_or_create(

            usuario=usuario,

            prato=prato,

            defaults={
                "nota": rating,
                "interesse": interesse,
                "status": status,

                # Só colocamos a data se ela existir.
                **(
                    {"data": data}
                    if data is not None
                    else {}
                )
            }
        )

        quantidade += 1

    print(
        f"{quantidade} interações criadas."
    )


# ============================================================
# EXECUÇÃO
# ============================================================

def main():

    print("\n")
    print("=" * 60)
    print("        POPULANDO BANCO - PRATOMATCH")
    print("=" * 60)

    limpar_banco()

    categorias = criar_categorias()

    alergias = criar_alergias()

    preferencias = criar_preferencias()

    usuarios = criar_usuarios()

    pratos = criar_pratos(usuarios)

    criar_perfis(
        usuarios,
        alergias,
        preferencias,
        categorias
    )

    criar_interacoes(
        usuarios,
        pratos
    )

    print("\n")
    print("=" * 60)
    print("        BANCO POPULADO COM SUCESSO!")
    print("=" * 60)

    print("\nResumo:")

    print(
        f"Usuários: {User.objects.count()}"
    )

    print(
        f"Perfis: {PerfilUsuario.objects.count()}"
    )

    print(
        f"Pratos: {Prato.objects.count()}"
    )


    print(
        f"Categorias: {Categoria.objects.count()}"
    )

    print(
        f"Alergias: {Alergia.objects.count()}"
    )

    print(
        f"Preferências: {PreferenciaAlimentar.objects.count()}"
    )

    print(
        f"Interações: {Interacao.objects.count()}"
    )

    print("\nUsuários de teste:")

    for usuario in usuarios.values():

        print(
            f"  {usuario.username} "
            f"(senha: 123456)"
        )

    print("\n")
    

if __name__ == "__main__":
    main()