from pathlib import Path
import pandas as pd
import sqlite3
import random
import os
import sys


# ============================================================
# CONFIGURAÇÃO DO DJANGO
# ============================================================

BASE_DIR_DJANGO = Path(__file__).resolve().parents[1]
DJANGO_DIR = BASE_DIR_DJANGO / "PratoMatch"

sys.path.insert(0, str(DJANGO_DIR))

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "configs.settings"
)


# ============================================================
# IMPORTA O ALGORITMO EXISTENTE
# ============================================================

from algoritmos import _obter_recomendacoes


# ============================================================
# CAMINHOS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]

CAMINHO_BANCO = BASE_DIR / "PratoMatch" / "db.sqlite3"

CAMINHO_RAW = BASE_DIR / "dataset" / "RAW_recipes.csv"

CAMINHO_INGR_MAP = BASE_DIR / "dataset" / "ingr_map.pkl"


# ============================================================
# HIT RATE@5
# ============================================================

def hit_rate_at_5(
    quantidade_usuarios=20,
    nota_relevante=4,
    quantidade_escondida=2,
):

    conexao = sqlite3.connect(CAMINHO_BANCO)

    try:

        # ====================================================
        # CARREGAR DADOS DO BANCO
        # ====================================================

        lista = pd.read_sql(
            "SELECT * FROM myapp_perfilusuario",
            conexao
        )

        lista_receitas = pd.read_sql(
            "SELECT * FROM myapp_prato",
            conexao
        )

        interacoes = pd.read_sql(
            "SELECT * FROM myapp_interacao",
            conexao
        )

        lista_escolhas_onboarding = pd.read_sql(
            "SELECT * FROM myapp_onboardingprato",
            conexao
        )


        # ====================================================
        # CARREGAR RECEITAS
        # ====================================================

        raw_receitas = pd.read_csv(
            CAMINHO_RAW
        ).set_index("id")


        # ====================================================
        # CARREGAR ingr_map UMA VEZ
        # ====================================================

        lista_trocas = pd.read_pickle(
            CAMINHO_INGR_MAP
        ).set_index("raw_ingr")


        # ====================================================
        # ORGANIZAR INTERAÇÕES POR USUÁRIO
        # ====================================================

        interacoes_por_usuario = (
            interacoes
            .groupby("usuario_id")["prato_id"]
            .apply(list)
        )

        notas_por_usuario = (
            interacoes
            .groupby("usuario_id")["nota"]
            .apply(list)
        )

        interacoes = interacoes.set_index("id")


        lista["items"] = lista["usuario_id"].apply(
            lambda usuario_id:
                interacoes_por_usuario.get(usuario_id, [])
        )

        lista["ratings"] = lista["usuario_id"].apply(
            lambda usuario_id:
                notas_por_usuario.get(usuario_id, [])
        )

        lista = lista.set_index("usuario_id")


        # ====================================================
        # ENCONTRAR USUÁRIOS ELEGÍVEIS
        # ====================================================

        usuarios_validos = []

        for usuario_id in lista.index:

            itens = lista.at[usuario_id, "items"]

            notas = lista.at[usuario_id, "ratings"]

            relevantes = [
                item
                for item, nota in zip(itens, notas)
                if float(nota) >= nota_relevante
            ]

            if len(relevantes) >= quantidade_escondida:

                usuarios_validos.append(usuario_id)


        if len(usuarios_validos) == 0:

            print("Nenhum usuário elegível encontrado.")

            return None


        # ====================================================
        # ESCOLHER USUÁRIOS PARA TESTE
        # ====================================================

        quantidade = min(
            quantidade_usuarios,
            len(usuarios_validos)
        )

        usuarios_teste = random.sample(
            usuarios_validos,
            quantidade
        )


        # ====================================================
        # CONTADORES
        # ====================================================

        hits = 0

        usuarios_avaliados = 0


        # ====================================================
        # TESTAR CADA USUÁRIO
        # ====================================================

        for usuario_id in usuarios_teste:

            # ----------------------------------------------
            # GUARDAR HISTÓRICO ORIGINAL
            # ----------------------------------------------

            itens_originais = lista.at[
                usuario_id,
                "items"
            ].copy()

            notas_originais = lista.at[
                usuario_id,
                "ratings"
            ].copy()


            # ----------------------------------------------
            # ENCONTRAR RECEITAS RELEVANTES
            # ----------------------------------------------

            relevantes = [
                item
                for item, nota in zip(
                    itens_originais,
                    notas_originais
                )
                if float(nota) >= nota_relevante
            ]


            # ----------------------------------------------
            # ESCOLHER RECEITAS QUE SERÃO ESCONDIDAS
            # ----------------------------------------------

            escondidas = random.sample(
                relevantes,
                quantidade_escondida
            )


            # ----------------------------------------------
            # REMOVER AS ESCONDIDAS DO HISTÓRICO
            # ----------------------------------------------

            novos_itens = []

            novas_notas = []

            for item, nota in zip(
                itens_originais,
                notas_originais
            ):

                if item not in escondidas:

                    novos_itens.append(item)

                    novas_notas.append(nota)


            lista.at[
                usuario_id,
                "items"
            ] = novos_itens

            lista.at[
                usuario_id,
                "ratings"
            ] = novas_notas


            try:

                # ==========================================
                # GERAR RECOMENDAÇÕES
                # ==========================================

                resultado = _obter_recomendacoes(

                    id=usuario_id,

                    k=100,

                    limite=5,

                    valorizacao_de_frequencia=0.2,

                    alergias=[],

                    alergias_dict={},

                    lista_escolhas_onboarding=(
                        lista_escolhas_onboarding
                    ),

                    lista=lista,

                    lista_receitas=lista_receitas,

                    interacoes=interacoes,

                    raw_receitas=raw_receitas,

                    lista_trocas=lista_trocas,

                    minimo_de_avaliacoes_pro_mesmo_prato_pra_nao_desconsiderar=1,

                    minimo_de_receitas_registradas_pra_nao_usar_as_do_onboarding=1,

                )


                # ==========================================
                # PEGAR AS 5 RECOMENDAÇÕES
                # ==========================================

                recomendados = (
                    resultado["prato_id"]
                    .head(5)
                    .tolist()
                )


                # ==========================================
                # VERIFICAR SE HOUVE PELO MENOS UM ACERTO
                # ==========================================

                acertos = [
                    prato
                    for prato in recomendados
                    if prato in escondidas
                ]


                teve_hit = len(acertos) > 0


                if teve_hit:

                    hits += 1


                usuarios_avaliados += 1


                # ==========================================
                # MOSTRAR RESULTADO DO USUÁRIO
                # ==========================================

                print(
                    f"\nUsuário {usuario_id}"
                    f"\n  Escondidas: {escondidas}"
                    f"\n  Recomendadas: {recomendados}"
                    f"\n  Acertos: {len(acertos)}"
                    f"\n  Hit@5: {'SIM' if teve_hit else 'NÃO'}"
                )


            finally:

                # ==========================================
                # RESTAURAR HISTÓRICO ORIGINAL
                # ==========================================

                lista.at[
                    usuario_id,
                    "items"
                ] = itens_originais

                lista.at[
                    usuario_id,
                    "ratings"
                ] = notas_originais


        # ====================================================
        # CÁLCULO FINAL
        # ====================================================

        hit_rate = (
            hits / usuarios_avaliados
            if usuarios_avaliados > 0
            else 0
        )


        # ====================================================
        # RESULTADO
        # ====================================================

        print("\n===================================")
        print("RESULTADO FINAL")
        print("===================================")

        print(
            f"Usuários avaliados: "
            f"{usuarios_avaliados}"
        )

        print(
            f"Usuários com pelo menos 1 acerto: "
            f"{hits}"
        )

        print(
            f"Hit Rate@5: "
            f"{hit_rate:.4f}"
        )

        print(
            f"Hit Rate@5 (%): "
            f"{hit_rate * 100:.2f}%"
        )

        print("===================================")


        return hit_rate


    finally:

        conexao.close()


# ============================================================
# EXECUÇÃO
# ============================================================

if __name__ == "__main__":

    hit_rate_at_5(
        quantidade_usuarios=20,
        nota_relevante=4,
        quantidade_escondida=2,
    )