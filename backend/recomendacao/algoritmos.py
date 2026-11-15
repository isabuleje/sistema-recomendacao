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

#ADICIONAR ESSES NO REQUIREMENTS DEPOIS
from sklearn.feature_extraction.text import TfidfVectorizer # (pip install scikit-learn)
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors

#from backend.PratoMatch.myapp.views import ingredientes

BASE_DIR_DJANGO = Path(__file__).resolve().parents[1]
DJANGO_DIR = BASE_DIR_DJANGO / "PratoMatch"

sys.path.insert(0, str(DJANGO_DIR))

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "configs.settings"
)

def tf_idf(base: sqlite3.Connection) -> pd.DataFrame:

    #temporario
    receitas = pd.read_csv("backend/dataset/PP_recipes.csv", usecols=["id", "ingredient_ids"]).head(1000)

    tfidf = TfidfVectorizer(token_pattern=r"\d+")
    X = tfidf.fit_transform(receitas["ingredient_ids"].astype(str))

    k = 10
    modelo = NearestNeighbors(n_neighbors=k + 1, metric="cosine", algorithm="brute", n_jobs=-1)
    modelo.fit(X)
    distancias, indices = modelo.kneighbors(X)

    ids = receitas["id"].to_numpy()
    similares = pd.DataFrame({
        "id": ids.repeat(k),
        "vizinho_id": ids[indices[:, 1:]].ravel(),
        "similaridade": (1 - distancias[:, 1:]).ravel(),
    })
    
    return similares

print(tf_idf(None))