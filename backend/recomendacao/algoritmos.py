from pathlib import Path
import pandas as pd
from pandas.core.frame import DataFrame
import ast
from decimal import Decimal

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
    return lista.loc[id]


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
    coef: float
    try:
        coef = produto / (comprimento(lista_1_comum) * comprimento(lista_2_comum))
    except (ZeroDivisionError):
        coef = 0.0
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

def lista_vizinhos(id: int, lista: DataFrame = None, fazer_print: bool = False) -> DataFrame:
    final: dict = {'u': [], 'similaridade': []}
    if lista is None:
        lista: DataFrame = pd.read_csv("backend/dataset/PP_users.csv")
    for id2 in lista['u']:
        similaridade: float = id_similaridade_cosseno(id, id2, lista)
        if similaridade > 0.0:
            if id != id2:
                if fazer_print:
                    print(id, ":", id2, "| grau de similaridade de cosseno:", similaridade)
                final['u'].append(id2)
                final['similaridade'].append(Decimal(similaridade))
    if fazer_print:
        print("fim")
    return DataFrame(final).sort_values('similaridade')

def k_nn(id: int, k: int = 3, lista: DataFrame = None, fazer_print: bool = False) -> DataFrame:
    if lista is None:
        lista: DataFrame = pd.read_csv("backend/dataset/PP_users.csv")
    vizinhos: DataFrame = lista_vizinhos(id, lista, fazer_print).iloc[-k:].iloc[::-1]
    tabela_influencia: dict = {'u':[], 'influencia':[]}
    total: Decimal = sum(vizinhos['similaridade'])
    for linha in vizinhos['u']:
        tabela_influencia['u'].append(linha)
        tabela_influencia['influencia'].append(vizinhos.loc[vizinhos['u'] == linha, 'similaridade'].item() / total)
    return DataFrame(tabela_influencia)

def obter_recomendacoes(id: int, k: int = 3, limite: int = 50, lista: DataFrame = None):
    if lista is None:
            lista: DataFrame = pd.read_csv("backend/dataset/PP_users.csv")
    receitas_usuario: list[int] = ast.literal_eval(obter_usuario_preload(id, lista)['items'])
    tabela_vizinhos: DataFrame = k_nn(id, k, lista)
    receitas_novas: dict[int, list] = {} #{id da receita ('i') : [quantas vezes apareceu, soma da nota recebida]}
    maior_frequencia: int = 0
    for vizinho, influencia in zip(tabela_vizinhos['u'], tabela_vizinhos['influencia']):
        possiveis_receitas = ast.literal_eval(obter_usuario_preload(vizinho, lista)['items'])
        receitas_notas = zip(possiveis_receitas, ast.literal_eval(obter_usuario_preload(vizinho, lista)['ratings']))
        for receita, nota in receitas_notas:
            if not receita in receitas_usuario:
                if receita in receitas_novas:
                    receitas_novas[receita][0] += 1
                    if receitas_novas[receita][0] > maior_frequencia:
                        maior_frequencia = receitas_novas[receita][0]
                    receitas_novas[receita][1] += Decimal(nota) * (influencia * Decimal(k))
                else:
                    receitas_novas[receita] = [1, Decimal(nota) * (influencia * Decimal(k))]
                    if maior_frequencia == 0:
                        maior_frequencia = 1
    for receita in receitas_novas:
        #{id da receita ('i') : soma da nota recebida / quantas vezes apareceu}
        receitas_novas[receita] = (float(receitas_novas[receita][1]) / receitas_novas[receita][0])
    return DataFrame(receitas_novas.items(), columns=['u', 'nota_esperada']).sort_values('nota_esperada')[-limite:][::-1]
print(obter_recomendacoes(id=1, k=3, limite=50))