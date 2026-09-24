from pathlib import Path
import pandas as pd
import pickle

BASE_DIR = Path(__file__).resolve().parent.parent

def load_data(file_path):
    try:
        data = pd.read_pickle(file_path)
        return data
    except Exception as e:
        print(f"Erro ao carregar os dados: {e}")
        return None

#Pra toda função que precisar dos dados, é só usar o RECEITAS
receitas = load_data(BASE_DIR / "dataset" / "ingr_map.pkl")


def carregar_ingredientes(data):
    if data is not None:
        return data["raw_ingr"].tolist()

    print("DataFrame não carregado. Não é possível obter as colunas.")
    return []

def carregar_ingredientes_por_prato(data):
    if data is not None:
        return data[["name", "raw_ingr"]].to_dict(orient="records")

    print("DataFrame não carregado. Não é possível obter as colunas.")
    return []



print(carregar_ingredientes_por_prato(receitas))