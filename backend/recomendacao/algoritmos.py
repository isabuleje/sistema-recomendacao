from pathlib import Path
import pandas as pd
import ast
from decimal import Decimal
import sqlite3
import time
import random
import os
import sys
from pathlib import Path
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer # (pip install scikit-learn)
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors

#from backend.PratoMatch.myapp.views import ingredientes

PASTA_ATUAL = Path(__file__).resolve().parent
PASTA_BACKEND = PASTA_ATUAL.parent
PASTA_DATASET = PASTA_BACKEND / "dataset"

ARQUIVO_RECEITAS = PASTA_DATASET / "PP_recipes.csv"


def tf_idf(receitas: pd.DataFrame):
    tfidf = TfidfVectorizer(token_pattern=r"\d+", dtype=np.float32)
    X = tfidf.fit_transform(receitas["ingredient_ids"].astype(str))
    return tfidf, X

def ranking_receitas_usuario(id_usuario, interacoes, receitas, X, n=10):
    ids = receitas["id"].to_numpy()
    linha_da_receita = pd.Series(np.arange(len(ids)), index=ids)

    # interações desse usuário, só com receitas que estão na matriz
    inter = interacoes[interacoes["usuario_id"] == id_usuario]
    inter = inter[inter["prato_id"].isin(linha_da_receita.index)]
    if inter.empty:
        return pd.DataFrame(columns=["id", "score"])

    linhas = linha_da_receita[inter["prato_id"]].to_numpy()
    pesos = inter["nota"].to_numpy(dtype=np.float32)

    # perfil: soma das receitas que ele avaliou, ponderada pela nota
    perfil = np.asarray(X[linhas].T.dot(pesos)).ravel()

    # score de cada receita = similaridade com o perfil
    scores = np.asarray(X.dot(perfil)).ravel()
    scores[linhas] = -np.inf  # não recomenda o que ele já avaliou

    top = np.argsort(-scores)[:n]
    return pd.DataFrame({"id": ids[top], "score": scores[top]})

def recomendar_para(id_usuario: int, conexao: sqlite3.Connection):
    receitas = pd.read_csv(ARQUIVO_RECEITAS, usecols=["id", "ingredient_ids"])
    tfidf, X = tf_idf(receitas)
    interacoes = pd.read_sql("SELECT * FROM myapp_interacao", conexao)
    return ranking_receitas_usuario(id_usuario, interacoes, receitas, X)

"""
conexao = sqlite3.connect("backend/PratoMatch/db.sqlite3")
#print(receita_ranking_por_usuario(conexao), 11))
receitas = pd.read_csv(ARQUIVO_RECEITAS, usecols=["id", "ingredient_ids"])
tfidf, X = tf_idf(receitas)
interacoes = pd.read_sql("SELECT * FROM myapp_interacao", conexao)
id_teste = interacoes["usuario_id"].value_counts().index[0]
ranking = ranking_receitas_usuario(id_teste, interacoes, receitas, X)
print(ranking)
"""
if __name__ == "__main__":
    print(recomendar_para(11, sqlite3.connect("backend/PratoMatch/db.sqlite3")))