"""Avalia uma base demonstrativa; os resultados não são benchmark real."""

import argparse
import json
import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd

from recomendacao.algoritmos import ranking_receitas_usuario, tf_idf
from recomendacao.metricas import (
    cobertura_catalogo,
    ndcg_at_k,
    precision_at_k,
    recall_at_k,
)
from recomendacao.metricas.baselines import (
    avaliar_rankings,
    ranking_aleatorio,
    ranking_popular,
)


BANCO_METRICAS = (
    Path(__file__).resolve().parents[2]
    / "PratoMatch"
    / "db_metricas.sqlite3"
)


def avaliar_demo(k=5):
    if k < 1:
        raise ValueError("k deve ser maior ou igual a 1")
    if not BANCO_METRICAS.exists():
        raise FileNotFoundError(
            f"Base demonstrativa não encontrada: {BANCO_METRICAS}. "
            "Execute `python seed_metricas.py` primeiro."
        )

    conexao = sqlite3.connect(BANCO_METRICAS)
    try:
        coortes = pd.read_sql_query(
            "SELECT id, usuario_id FROM coorte ORDER BY id",
            conexao,
        )
        total_pratos = pd.read_sql_query(
            "SELECT COUNT(*) AS total FROM prato",
            conexao,
        ).iloc[0]["total"]
        metricas = {
            "precision": precision_at_k,
            "recall": recall_at_k,
            "ndcg": ndcg_at_k,
        }
        valores = {nome: [] for nome in metricas}
        rankings_baseline = {"aleatorio": {}, "popular": {}}
        relevantes = {}
        recomendacoes_totais = []
        rng = np.random.default_rng(42)

        for coorte in coortes.itertuples(index=False):
            usuario_id = int(coorte.usuario_id)
            pratos = pd.read_sql_query(
                """
                SELECT p.id, p.ingredient_ids
                FROM prato p
                JOIN coorte_prato cp ON cp.prato_id = p.id
                WHERE cp.coorte_id = ?
                ORDER BY p.id
                """,
                conexao,
                params=(int(coorte.id),),
            )
            treino = pd.read_sql_query(
                """
                SELECT usuario_id, prato_id, nota, tempo_visualizado
                FROM interacao
                WHERE usuario_id = ? AND split = 'treino'
                """,
                conexao,
                params=(usuario_id,),
            )
            teste = pd.read_sql_query(
                """
                SELECT prato_id
                FROM interacao
                WHERE usuario_id = ? AND split = 'teste' AND nota >= 4
                """,
                conexao,
                params=(usuario_id,),
            )
            itens_relevantes = set(teste["prato_id"].astype(int))
            if treino.empty or not itens_relevantes:
                raise ValueError(
                    f"A coorte {coorte.id} precisa de treino e de pelo "
                    "menos um item relevante no teste."
                )

            conhecidos = set(treino["prato_id"].astype(int))
            _, matriz = tf_idf(pratos)
            ranking = ranking_receitas_usuario(
                usuario_id,
                treino,
                pratos,
                matriz,
                conexao,
                n=k,
            )
            recomendacoes = ranking["id"].astype(int).tolist()
            recomendacoes_totais.extend(recomendacoes)
            relevantes[usuario_id] = itens_relevantes

            for nome, funcao in metricas.items():
                valores[nome].append(
                    funcao(recomendacoes, itens_relevantes, k)
                )

            ids_catalogo = sorted(pratos["id"].astype(int))
            rankings_baseline["aleatorio"][usuario_id] = ranking_aleatorio(
                ids_catalogo,
                conhecidos,
                rng,
                k,
            )
            rankings_baseline["popular"][usuario_id] = ranking_popular(
                treino,
                conhecidos,
                k,
            )
    finally:
        conexao.close()

    return {
        "origem": "demonstracao_sintetica",
        "usuarios": len(relevantes),
        "k": k,
        "precision": float(np.mean(valores["precision"])),
        "recall": float(np.mean(valores["recall"])),
        "ndcg": float(np.mean(valores["ndcg"])),
        "cobertura_catalogo": cobertura_catalogo(
            recomendacoes_totais,
            int(total_pratos),
        ),
        "baselines": avaliar_rankings(
            rankings_baseline,
            relevantes,
            k,
            metricas,
        ),
        "aviso": (
            "Dados sintéticos para demonstração; não representam "
            "desempenho real do sistema."
        ),
    }


def main():
    parser = argparse.ArgumentParser(
        description="Calcula métricas na base demonstrativa isolada."
    )
    parser.add_argument("-k", type=int, default=5)
    args = parser.parse_args()
    if args.k < 1:
        parser.error("-k deve ser maior ou igual a 1")
    print(json.dumps(avaliar_demo(args.k), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
