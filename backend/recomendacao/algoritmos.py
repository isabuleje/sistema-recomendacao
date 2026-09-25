from pathlib import Path
import pandas as pd
from pandas.core.frame import DataFrame
import ast

#constantes
#MINIMO_DE_RECEITAS_EM_COMUM_PARA_AVALIAR_SEMELHANCA = 5
MINIMO_EM_COMUM = 3


#funções auxiliares

def obter_usuario(id: int) -> dict:
    lista: DataFrame = pd.read_csv("backend/dataset/PP_users.csv")
    return lista.loc[id]

#se for chamar a função várias vezes seguidas, usar essa aqui por favor
def obter_usuario_preload(id: int, lista: DataFrame):
    return lista.loc[id]
    return lista[lista['u'] == id]

def obter_receita(id: int) -> dict:
    lista: dict = pd.read_csv("backend/dataset/PP_recipes.csv")
    #'i' = equivalente aos indices que a coluna 'items' do PP_users.csv representa
    #'id' = equivalente aos indices que a coluna 'id' no RAW_recipes.csv representa
    return lista[lista['i'] == id]

def obter_receita_RAW(id: int) -> dict:
    lista = pd.read_csv("backend/dataset/RAW_recipes.csv")
    return lista[lista['id'] == id]



def calcular_similaridade_cosseno(lista_1: list[float], idxlista_1: list[int], lista_2: list[float], idxlista_2: list[int]) -> float:
    lista_1_comum: list[float] = []
    lista_2_comum: list[float] = []

    mapa2 = {idx:nota for idx, nota in zip(idxlista_2, lista_2)}
    for idx, nota in zip(idxlista_1, lista_1):
        if idx in mapa2:
            lista_1_comum.append(nota)
            lista_2_comum.append(mapa2[idx])

    if len(lista_1_comum) < MINIMO_EM_COMUM:
        return 0.0

    # (X * Y)
    produto: float = (sum(x * y for x, y in zip(lista_1_comum, lista_2_comum)))
    # ||X||
    comprimento: callable = lambda lista: (sum(x ** 2 for x in lista) ** 0.5)
    # (X * Y) / (||X|| * ||Y||)          
    coef: float = produto / (comprimento(lista_1_comum) * comprimento(lista_2_comum))
    return coef

#usando id ('u') de usuário de PP_users.csv
#usar lista pré-carregada sempre que possível por favor
def id_similaridade_cosseno(id_usuario_1: int, id_usuario_2: int, lista: DataFrame = None) -> float:
    if lista is None:
        usuario1 = obter_usuario(id_usuario_1)
        usuario2 = obter_usuario(id_usuario_2)
    else:
        usuario1 = obter_usuario_preload(id_usuario_1, lista)
        usuario2 = obter_usuario_preload(id_usuario_2, lista)
    return calcular_similaridade_cosseno(
        ast.literal_eval(usuario1['ratings']),
        ast.literal_eval(usuario1['items']),
        ast.literal_eval(usuario2['ratings']),
        ast.literal_eval(usuario2['items'])
    )

def vizinhos_knn(id: int, fazer_print: bool = False) -> DataFrame:
    final: dict = {'u': [], 'similaridade': []}
    lista: DataFrame = pd.read_csv("backend/dataset/PP_users.csv")
    for id2 in lista['u']:
        similaridade: float = id_similaridade_cosseno(id, id2, lista)
        if similaridade > 0.0:
            if id != id2:
                if fazer_print:
                    print(id, ":", id2, "| grau de similaridade de cosseno:", similaridade)
                final['u'].append(id2)
                final['similaridade'].append(similaridade)
    if fazer_print:
        print("fim")
    return DataFrame(final)

print(vizinhos_knn(id=1, fazer_print=True))