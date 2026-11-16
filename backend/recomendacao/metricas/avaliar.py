import argparse
import json
from pathlib import Path
import pandas as pd
from recomendacao.algoritmos import ranking_receitas_usuario, tf_idf
from recomendacao.metricas import (cobertura_catalogo, ndcg_at_k, precision_at_k, recall_at_k,)

#Pra rodar usar: python -m recomendacao.metricas.avaliar (na base do backend)

DATASET = Path(__file__).resolve().parents[2] / "dataset"

def avaliar(k=10, nota_minima=4, limite_usuarios=None):
    #esses caminhos com ctz vao dar problema xd
    receitas = pd.read_csv(DATASET / "PP_recipes.csv", usecols=["id", "ingredient_ids"])
    treino = pd.read_csv(DATASET / "interactions_train.csv", usecols=["user_id", "recipe_id", "rating"])
    teste = pd.read_csv(DATASET / "interactions_test.csv", usecols=["user_id", "recipe_id", "rating"])

    # Padroniza os nomes das colunas
    treino = treino.rename(columns={"user_id": "usuario_id", "recipe_id": "prato_id", "rating": "nota",})
r
    # Padroniza os tipos dos identificadores
    receitas["id"] = pd.to_numeric(receitas["id"], errors="coerce")
    treino["usuario_id"] = pd.to_numeric(treino["usuario_id"], errors="coerce")
    treino["prato_id"] = pd.to_numeric(treino["prato_id"], errors="coerce")
    teste["user_id"] = pd.to_numeric(teste["user_id"], errors="coerce")
    teste["recipe_id"] = pd.to_numeric(teste["recipe_id"], errors="coerce")

    receitas = receitas.dropna(subset=["id"]).copy()
    treino = treino.dropna(subset=["usuario_id", "prato_id"]).copy()
    teste = teste.dropna(subset=["user_id", "recipe_id"]).copy()

    receitas["id"] = receitas["id"].astype(int)
    treino["usuario_id"] = treino["usuario_id"].astype(int)
    treino["prato_id"] = treino["prato_id"].astype(int)
    teste["user_id"] = teste["user_id"].astype(int)
    teste["recipe_id"] = teste["recipe_id"].astype(int)

    # Remove duplicatas do catálogo
    receitas = receitas.drop_duplicates(subset=["id"])

    # Coluna necessária pelo algoritmo
    treino["tempo_visualizado"] = 0

    ids_receitas = set(receitas["id"])

    # Remove interações com receitas fora do catálogo
    treino = treino[treino["prato_id"].isin(ids_receitas)]
    teste = teste[teste["recipe_id"].isin(ids_receitas)]

    # Receitas relevantes no conjunto de teste
    relevantes = {
        usuario: set(
            grupo.loc[
                grupo["rating"] >= nota_minima,
                "recipe_id"
            ]
        )
        for usuario, grupo in teste.groupby("user_id")
    }

    # Usuários que possuem histórico e receitas relevantes
    usuarios_treino = set(treino["usuario_id"])
    usuarios = sorted(
        usuario
        for usuario, itens in relevantes.items()
        if itens and usuario in usuarios_treino
    )

    if limite_usuarios is not None:
        usuarios = usuarios[:limite_usuarios]

    if not usuarios:
        raise ValueError(
            "Nenhum usuário possui histórico de treino e receitas "
            "relevantes no conjunto de teste."
        )

    # Constrói a matriz TF-IDF
    _, matriz = tf_idf(receitas)

    rankings = {}
    tamanhos_ranking = []
    for usuario in usuarios:
        # Receitas já conhecidas pelo usuário
        conhecidas = set(
            treino.loc[
                treino["usuario_id"] == usuario,
                "prato_id"
            ]
        )

        # Gera recomendações
        ranking = ranking_receitas_usuario(
            usuario,
            treino,
            receitas,
            matriz,
            n=len(ids_receitas),
        )

        # Exclui receitas já avaliadas
        ranking = ranking[~ranking["id"].isin(conhecidas)]

        # Remove possíveis duplicatas
        ranking = ranking.drop_duplicates(subset=["id"])

        # Limita a quantidade de recomendações
        ranking = ranking.head(k)

        rankings[usuario] = ranking["id"].tolist()
        tamanhos_ranking.append(len(rankings[usuario]))

    # Calcula as métricas por usuário
    precisions = []
    recalls = []
    ndcgs = []

    for usuario in usuarios:

        recomendacoes = rankings[usuario]
        itens_relevantes = relevantes[usuario]

        precisions.append(precision_at_k(recomendacoes, itens_relevantes, k))
        recalls.append(recall_at_k(recomendacoes, itens_relevantes, k))
        ndcgs.append(ndcg_at_k(recomendacoes, itens_relevantes, k))

    # Todas as recomendações realizadas
    recomendacoes_totais = [
        item
        for ranking in rankings.values()
        for item in ranking
    ]

    # Diagnósticos
    total_relevantes = sum(
        len(relevantes[usuario])
        for usuario in usuarios
    )

    total_recomendacoes = len(recomendacoes_totais)

    return {
        "usuarios": len(usuarios),
        "k": k,
        "precision": sum(precisions) / len(precisions),
        "recall": sum(recalls) / len(recalls),
        "ndcg": sum(ndcgs) / len(ndcgs),
        "cobertura_catalogo": cobertura_catalogo(
            recomendacoes_totais,
            len(ids_receitas),
        ),
        "diagnostico": {
            "total_receitas_catalogo": len(ids_receitas),
            "total_recomendacoes": total_recomendacoes,
            "total_relevantes_teste": total_relevantes,
            "media_recomendacoes_por_usuario": (
                total_recomendacoes / len(usuarios)
            ),
            "media_relevantes_por_usuario": (
                total_relevantes / len(usuarios)
            ),
            "usuarios_com_ranking_completo": sum(
                tamanho == k for tamanho in tamanhos_ranking
            ),
            "usuarios_com_ranking_incompleto": sum(
                tamanho < k for tamanho in tamanhos_ranking
            ),
            "itens_unicos_recomendados": len(set(recomendacoes_totais)),
        },
    }


def main():

    parser = argparse.ArgumentParser(
        description="Avalia o recomendador TF-IDF com os CSVs reais."
    )

    parser.add_argument("-k", type=int, default=10)
    parser.add_argument("--nota-minima", type=float, default=4)
    parser.add_argument("--limite-usuarios", type=int)

    args = parser.parse_args()

    if args.k < 1:
        parser.error("-k deve ser maior ou igual a 1")

    if args.limite_usuarios is not None and args.limite_usuarios < 1:
        parser.error("--limite-usuarios deve ser maior que 0")

    resultado = avaliar(
        args.k,
        args.nota_minima,
        args.limite_usuarios,
    )

    print(json.dumps(resultado, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
