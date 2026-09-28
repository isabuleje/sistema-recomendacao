from pathlib import Path
import pandas as pd
from pandas.core.frame import DataFrame
import ast
from decimal import Decimal
import sqlite3
import time

#constantes
#MINIMO_DE_RECEITAS_EM_COMUM_PARA_AVALIAR_SEMELHANCA = 5

def obter_receita(id: int) -> dict:
    lista: dict = pd.read_csv("backend/dataset/PP_recipes.csv")
    #'i' = equivalente aos indices que a coluna 'items' do PP_users.csv representa
    #'id' = equivalente aos indices que a coluna 'id' no RAW_recipes.csv representa
    return lista.loc[id]


def calcular_similaridade_cosseno(lista_1: list[float], idxlista_1: list[int], lista_2: list[float], idxlista_2: list[int], min: int = 3) -> float:
    lista_1_comum: list[float] = []
    lista_2_comum: list[float] = []

    mapa2 = {idx:nota for idx, nota in zip(idxlista_2, lista_2)}
    for idx, nota in zip(idxlista_1, lista_1):
        if idx in mapa2:
            lista_1_comum.append(nota)
            lista_2_comum.append(mapa2[idx])
    if len(lista_1_comum) < min:
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
def id_similaridade_cosseno(id_usuario_1: int, id_usuario_2: int, lista: DataFrame | None = None, min: int = 3) -> float:
    if lista is None:
        raise Exception('faltou lista pra usar pra calcular similaridades')
    #print(lista.loc[id_usuario_1])
    try:
        usuario1 = lista.loc[id_usuario_1]
        usuario2 = lista.loc[id_usuario_2]
    except (KeyError):
        #print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaabbbbbbbbbbbbbbbbb")
        return 0.0
    
    #DEPOIS COMENTAR TODOS ESSES PRINTS MAS NAO APAGAR CASO EU PRECISE CAÇAR MAIS BUG
    """print('\n\n')
    #print(f'tipo de dado dos elementos da lista só pra ter certeza que n é por isso algum problema: {type(usuario1['items'][0])}')
    print(f'testando interseção nas receitas avaliadas pelos usuarios com ids {id_usuario_1} x {id_usuario_2}:')
    #print(f'ids de receita que {id_usuario_1} avaliou: {usuario1['items']}')
    #print(f'ids de receita que {id_usuario_2} avaliou: {usuario2['items']}')
    n = 0
    for item in (usuario1['items']):
        if item in usuario2['items'] and not id_usuario_1 == id_usuario_2:
            n+=1
            print(f'usuario com id {id_usuario_1} e usuario com id {id_usuario_2} tinham em comum o item {item} avaliado')
    print(f'eles tinham {n} ite{'m' if (n == 1) else 'ns'} avaliado{'' if (n == 1) else 's'} em comum')"""
    #FIM DA PARTE PRA DEIXAR COMENTADA

    return calcular_similaridade_cosseno(
        (usuario1['ratings']),
        (usuario1['items']),
        (usuario2['ratings']),
        (usuario2['items']),
        min=min
    )

def lista_vizinhos(id: int, lista: DataFrame | None = None, fazer_print: bool = False, min: int = 3) -> DataFrame:
    final: dict = {'u': [], 'similaridade': []}
    for id2 in lista.index:
        #print("buhuajfjii:", id2)
        #print(lista.loc[id2])
        similaridade: float = id_similaridade_cosseno(id, id2, lista, min)
        #print(similaridade)
        if similaridade > 0.0:
            if id != id2:
                if fazer_print:
                    print(id, ":", id2, "| grau de similaridade de cosseno:", similaridade)
                final['u'].append(id2)
                final['similaridade'].append(Decimal(similaridade))
    if fazer_print:
        print("fim")
    return DataFrame(final).sort_values('similaridade')

def k_nn(id: int, k: int = 3, lista: DataFrame | None = None, fazer_print: bool = False, min: int = 3) -> DataFrame:
    vizinhos: DataFrame = lista_vizinhos(id, lista, fazer_print, min).iloc[-k:].iloc[::-1]
    tabela_influencia: dict = {'u':[], 'influencia':[]}
    total: Decimal = sum(vizinhos['similaridade'])
    for linha in vizinhos['u']:
        tabela_influencia['u'].append(linha)
        tabela_influencia['influencia'].append(vizinhos.loc[vizinhos['u'] == linha, 'similaridade'].item() / total)
    return DataFrame(tabela_influencia)

def obter_recomendacoes(id: int, k: int = 3, limite: int = 50, valorizacao_de_frequencia: float = 0.1, conexao: sqlite3.Connection | None = None, raw_receitas: DataFrame = DataFrame(), minimo_de_avaliacoes_pro_mesmo_prato_pra_nao_desconsiderar: int = 3, imprimir_metricas: bool = False):
    if conexao is None:
        return None
    if imprimir_metricas:
        inicio = time.perf_counter()
        print(f"INICIO DO ALGORITMO DE BUSCA DE RECOMENDAÇÕES PARA USUÁRIO ID: {id}")
    lista: DataFrame = (pd.read_sql("SELECT * FROM myapp_perfilusuario", con=conexao))
    lista_receitas: DataFrame = pd.read_sql("SELECT * FROM myapp_prato", con=conexao)
    interacoes: DataFrame = pd.read_sql("SELECT * FROM myapp_interacao", con=conexao)
    if imprimir_metricas:
        print(f'{time.perf_counter() - inicio} S: LISTAS TRANSFERIDAS DE SQL PARA PANDAS')
    #parte que seria mt mais facil se cada usuario na tabela usuario guardasse uma lista com as interacoes que ele fez
    interacoes_por_id_de_usuario: DataFrame = interacoes.groupby('usuario_id')['prato_id'].apply(list)
    notas_por_id_de_usuario: DataFrame = interacoes.groupby('usuario_id')['nota'].apply(list)
    interacoes = interacoes.set_index('id')
    lista['items'] = lista.apply(lambda linha: interacoes_por_id_de_usuario.get(linha['usuario_id'], []), axis=1)
    lista['ratings'] = lista.apply(lambda linha: notas_por_id_de_usuario.get(linha['usuario_id'], []), axis=1)
    lista = lista.set_index('usuario_id')
    if imprimir_metricas:
        print(f'{time.perf_counter() - inicio} S: LISTAS MODIFICADAS PRA SEREM USAVEIS MAIS EFICIENTEMENTE NO ALGORITMO')
    if not id in lista.index:
        print(lista)
        raise ValueError(f'Usuário com id {id} não encontrado ou não existe. ids na lista: {lista.index}')
    
    receitas_usuario: list[int] = (lista.at[id, 'items'])
    tabela_vizinhos: DataFrame = k_nn(id, k, lista, False, minimo_de_avaliacoes_pro_mesmo_prato_pra_nao_desconsiderar)
    receitas_novas: dict[int, list] = {} #{id da receita ('i') : [quantas vezes apareceu, soma da nota recebida]}
    receitas_frequencia: dict[int, int] = {}
    receitas_valor: dict[int, int] = {}
    maior_frequencia: int = 0
    for vizinho, influencia in zip(tabela_vizinhos['u'], tabela_vizinhos['influencia']):
        possiveis_receitas = (lista.at[vizinho, 'items'])
        receitas_notas = zip(possiveis_receitas, (lista.at[vizinho, 'ratings']))
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
    if imprimir_metricas:
        print(f'{time.perf_counter() - inicio} S: RECEITAS E DADOS BRUTOS DO k_NN OBTIDOS E ORGANIZADOS')
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

    placar: DataFrame = DataFrame((receitas_novas).items(), columns=['prato_id', 'nota_esperada'])
    placar['quantidade de avaliacoes'] = placar['prato_id'].map(receitas_frequencia)
    placar['valor interno de classificacao'] = placar['prato_id'].map(receitas_valor)
    placar = placar.sort_values('valor interno de classificacao', ascending=False)

#IMPORTANTE trocar a(s) proxima(s) linha(s) pela forma de obter os filtros de remoção pessoais do usuário quando a gente tiver o modelo do banco de dados
    filtro_ingredientes: list = ['egg']
    #filtro_valor_nutricional
    #filtro_data_de_publicacao_maxima_sei_la
    contador: int = 0
    contador_indice: int = 0
    while contador <= limite:
        try:
            receita_raw = (raw_receitas.loc[(lista_receitas.at[placar.at[contador_indice, 'prato_id'].item(), 'id']).item()])
        except(KeyError):
            break
        
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

    if imprimir_metricas:
        print(f'{time.perf_counter() - inicio} S: FILTROS FINAIS EXECUTADOS E ORGANIZAÇÃO DA LISTA FINAL DE RESPOSTAS PREPARADA. PROCESSO FINALIZADO')
    return placar.head(limite)


conexao = sqlite3.connect("backend/PratoMatch/db.sqlite3")

verificados = [12]
#descomentar pra testar com todos os usuarios que existem
#verificados = pd.read_sql("SELECT * FROM myapp_perfilusuario", con=conexao).set_index('usuario_id')
for usuario in verificados: print(f'\nid:{usuario}\n',
    obter_recomendacoes(
        id=usuario, k=100, limite=3, valorizacao_de_frequencia=0.2,
        conexao=sqlite3.connect("backend/PratoMatch/db.sqlite3"),
        raw_receitas=pd.read_csv("backend/dataset/RAW_recipes.csv").set_index('id'),
        minimo_de_avaliacoes_pro_mesmo_prato_pra_nao_desconsiderar=1,
        imprimir_metricas=True
        )
    )

#myapp_alergia
#myapp_categoria
#myapp_ingrediente
#myapp_prato
#myapp_perfilusuario_alergias
#myapp_perfilusuario_categorias_preferidas
#myapp_perfilusuario_preferencias
#myapp_interacao