from pathlib import Path
import pandas as pd
from pandas.core.frame import DataFrame
import ast
from decimal import Decimal

#constantes
#MINIMO_DE_RECEITAS_EM_COMUM_PARA_AVALIAR_SEMELHANCA = 5
MINIMO_EM_COMUM = 3

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
def id_similaridade_cosseno(id_usuario_1: int, id_usuario_2: int, lista: DataFrame = DataFrame()) -> float:
    if lista is None:
        lista: DataFrame = pd.read_csv("backend/dataset/PP_users.csv")
    try:
        usuario1 = lista.loc[id_usuario_1]
        usuario2 = lista.loc[id_usuario_2]
    except (KeyError):
        return 0.0
    
    return calcular_similaridade_cosseno(
        ast.literal_eval(usuario1['ratings']),
        ast.literal_eval(usuario1['items']),
        ast.literal_eval(usuario2['ratings']),
        ast.literal_eval(usuario2['items'])
    )

def lista_vizinhos(id: int, lista: DataFrame = DataFrame(), fazer_print: bool = False) -> DataFrame:
    final: dict = {'u': [], 'similaridade': []}
    if lista is None:
        lista: DataFrame = pd.read_csv("backend/dataset/PP_users.csv")
    for id2 in range(len(lista)):
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

def k_nn(id: int, k: int = 3, lista: DataFrame = DataFrame(), fazer_print: bool = False) -> DataFrame:
    vizinhos: DataFrame = lista_vizinhos(id, lista, fazer_print).iloc[-k:].iloc[::-1]
    tabela_influencia: dict = {'u':[], 'influencia':[]}
    total: Decimal = sum(vizinhos['similaridade'])
    for linha in vizinhos['u']:
        tabela_influencia['u'].append(linha)
        tabela_influencia['influencia'].append(vizinhos.loc[vizinhos['u'] == linha, 'similaridade'].item() / total)
    return DataFrame(tabela_influencia)

def obter_recomendacoes(id: int, k: int = 3, limite: int = 50, valorizacao_de_frequencia: float = 0.1, lista: DataFrame = DataFrame(), lista_receitas: DataFrame = DataFrame(), raw_receitas: DataFrame = DataFrame()):
    if lista is None:
            lista: DataFrame = pd.read_csv("backend/dataset/PP_users.csv")
    if not id in lista.index:
        raise ValueError(f'Usuário com id {id} não encontrado ou não existe')
    
    receitas_usuario: list[int] = ast.literal_eval(lista.at[id, 'items'])
    tabela_vizinhos: DataFrame = k_nn(id, k, lista)
    receitas_novas: dict[int, list] = {} #{id da receita ('i') : [quantas vezes apareceu, soma da nota recebida]}
    receitas_frequencia: dict[int, int] = {}
    receitas_valor: dict[int, int] = {}
    maior_frequencia: int = 0
    for vizinho, influencia in zip(tabela_vizinhos['u'], tabela_vizinhos['influencia']):
        possiveis_receitas = ast.literal_eval(lista.at[vizinho, 'items'])
        receitas_notas = zip(possiveis_receitas, ast.literal_eval(lista.at[vizinho, 'ratings']))
        for receita, nota in receitas_notas:
            if not receita in receitas_usuario:
                if receita in receitas_novas:
                    receitas_novas[receita][0] += 1
                    if receitas_novas[receita][0] > maior_frequencia:
                        maior_frequencia = receitas_novas[receita][0]
                    receitas_novas[receita][1] += (nota) * (float(influencia))
                    receitas_novas[receita][2] += influencia
                else:
                    receitas_novas[receita] = [1, (nota) * (float(influencia)), influencia]
                    if maior_frequencia == 0:
                        maior_frequencia = 1
    for receita in receitas_novas:
        receitas_frequencia[receita] = receitas_novas[receita][0]
        #{id da receita ('i') : soma da nota recebida / quantas vezes apareceu}
        frequencia = float(receitas_novas[receita][0])
        nota = float(receitas_novas[receita][1])
        nota_prevista: float =  nota / float(receitas_novas[receita][2])
        receitas_novas[receita] = nota_prevista
        if maior_frequencia == 1 or valorizacao_de_frequencia == 0.0:
            receitas_valor[receita] = nota_prevista
        else:
            receitas_valor[receita] = nota_prevista + (nota_prevista * valorizacao_de_frequencia * ((((frequencia - 1)/(maior_frequencia - 1)) ** 0.5)))

    placar: DataFrame = DataFrame((receitas_novas).items(), columns=['i', 'nota_esperada'])
    placar['quantidade de avaliacoes'] = placar['i'].map(receitas_frequencia)
    placar['valor interno de classificacao'] = placar['i'].map(receitas_valor)
    placar = placar.sort_values('valor interno de classificacao', ascending=False)

#IMPORTANTE trocar a(s) proxima(s) linha(s) pela forma de obter os filtros de remoção pessoais do usuário quando a gente tiver o modelo do banco de dados
    filtro_ingredientes: list = ['egg']
    #filtro_valor_nutricional
    #filtro_data_de_publicacao_maxima_sei_la
    contador: int = 0
    contador_indice: int = 0
    while contador <= limite:
        receita_raw = (raw_receitas.loc[(lista_receitas.at[placar.at[contador_indice, 'i'].item(), 'id']).item()])

        ingredientes_receita = receita_raw['ingredients']
        check: bool = True
        for ingrediente in filtro_ingredientes:
            if ingrediente in ingredientes_receita:
                check = False
                break
            #if ingrediente in lista_de_seila_alguma_outra_coisa
                #check = False
                #break
        if check:
            contador += 1
        else:
            print('tinha ovo nessa receita e ela foi pulada por causa da sua alergia\n', ingredientes_receita, '\nna verdade foi acidente a lista registrar como string mas serve pra coisas funcionarem no plural como egg ser parte de eggs. a receita era essa: id', placar.at[contador_indice, 'i'].item(), '\n')
            placar.drop(contador_indice, inplace = True)
        contador_indice += 1
    return placar.head(limite)
print(
    obter_recomendacoes(
        id=1, k=100, limite=50, valorizacao_de_frequencia=0.2,
        lista=pd.read_csv("backend/dataset/PP_users.csv").set_index('u'),
        lista_receitas=pd.read_csv("backend/dataset/PP_recipes.csv").set_index('i'),
        raw_receitas=pd.read_csv("backend/dataset/RAW_recipes.csv").set_index('id')
        )
    )

#se no final tiver só 1 banco de dados de receitas e não 2 vou ter que fazer umas alterações a mais
#mas vai ser facil ent se precisar pode só avisar
#o motivo de ter diferença de pp_recipes pra raw_recipes é que o PP é simplese o RAW tem
#informações quase nunca usadas no backend entao usar só os arquivos marcados PP pra fazer esse acesso
#sempre que não precisar de informação do RAW faz o código rodar mais rápido porque percorre uma lista mais simples
