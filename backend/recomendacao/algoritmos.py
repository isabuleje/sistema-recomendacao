from pathlib import Path
import pandas as pd
from pandas.core.frame import DataFrame
import ast
from decimal import Decimal
import sqlite3
import time
import random
import os
import sys
from pathlib import Path

BASE_DIR_DJANGO = Path(__file__).resolve().parents[1]
DJANGO_DIR = BASE_DIR_DJANGO / "PratoMatch"

sys.path.insert(0, str(DJANGO_DIR))

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "configs.settings"
)

#constantes
#MINIMO_DE_RECEITAS_EM_COMUM_PARA_AVALIAR_SEMELHANCA = 5
BASE_DIR = Path(__file__).resolve().parent.parent

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

def _obter_recomendacoes(id: int = 0, k: int = 3, limite: int = 50, valorizacao_de_frequencia: float = 0.1, alergias_dict: dict = {}, lista_escolhas_onboarding: DataFrame | None = None, lista: DataFrame | None = None, lista_receitas: DataFrame | None = None, interacoes: DataFrame | None = None, raw_receitas: DataFrame | None = None, alergias: list = [], minimo_de_avaliacoes_pro_mesmo_prato_pra_nao_desconsiderar: int = 3, imprimir_metricas: bool = False, minimo_de_receitas_registradas_pra_nao_usar_as_do_onboarding: int = 5):

    if imprimir_metricas:
        inicio = time.perf_counter()
        print(f"INICIO DO ALGORITMO DE BUSCA DE RECOMENDAÇÕES PARA USUÁRIO ID: {id}")

    if len(lista.loc[id]['items']) < minimo_de_receitas_registradas_pra_nao_usar_as_do_onboarding:
        faltando: int = minimo_de_receitas_registradas_pra_nao_usar_as_do_onboarding - len(lista.loc[id]['items'])

        escolhas: list = (lista_escolhas_onboarding.groupby('perfil_id')['prato_id'].apply(list)).get(id, [])
        #print(escolhas)
        for n in escolhas:
            if faltando == 0:
                break
            #print('adicionando coisas da coisa la porque faltou')
            lista.loc[id]['items'] = lista.loc[id]['items'].append(n)
            lista.loc[id]['ratings'] = lista.loc[id]['ratings'].append(5.0)
            faltando -= 1
        #print(lista.loc[id])
    if imprimir_metricas:
        print(f'{time.perf_counter() - inicio}s: LISTAS MODIFICADAS PRA SEREM USAVEIS MAIS EFICIENTEMENTE NO ALGORITMO')
    if not id in lista.index:
        print(lista)
        raise ValueError(f'Usuário com id {id} não encontrado ou não existe. ids na lista: {lista.index.to_list()}')
    
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
        print(f'{time.perf_counter() - inicio}s: RECEITAS E DADOS BRUTOS DO k_NN OBTIDOS E ORGANIZADOS')
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

    if len(placar) == 0:
        quantidade = min(limite * 2, len(lista_receitas))  
        sorteio = random.sample(list(lista_receitas.index), quantidade)
        placar = DataFrame({
            'prato_id': sorteio,
            'nota_esperada': 5.0,
            'quantidade de avaliacoes': 1,
            'valor interno de classificacao': 1.0,
        })

    lista_trocas = pd.read_pickle(BASE_DIR / "dataset" / "ingr_map.pkl").set_index('raw_ingr')
    #print(alergias_dict)
    #print(lista_trocas.loc['iceberg lettuce leaf']['replaced'])
    filtro_ingredientes: list = [lista_trocas.loc[alergias_dict[chave]]['replaced'] if alergias_dict[chave] in lista_trocas.index else alergias_dict[chave] for chave in alergias]
    #print(filtro_ingredientes)
    #filtro_valor_nutricional
    #filtro_data_de_publicacao_maxima_sei_la
    contador: int = 0
    contador_indice: int = 0
    passa: bool = len(filtro_ingredientes) > 0
    #print(lista_trocas)
    #trocas_agrupadas = lista_trocas.groupby('replaced')['raw_ingr'].apply(list)
    #print(trocas_agrupadas)
    while contador <= len(placar) and passa:
        try:
            receita: list = ast.literal_eval(raw_receitas.at[placar.at[contador_indice, 'prato_id'], 'ingredients'])
            #print(receita)
            receita = [lista_trocas.loc[chave]['replaced'] if chave in lista_trocas.index else chave for chave in receita]
            #print(receita)
        except(Exception):
            passa = False
            break
        if passa:
            #print(receita)
            check: bool = True
            for ingrediente in filtro_ingredientes:
                if ingrediente in receita:
                    check = False
                    break
                else:
                    #print("passou")
                    pass
                #if ingrediente in lista_de_seila_alguma_outra_coisa
                    #check = False
                    #break
            if check:
                contador += 1
            else:
                #print('tinha ovo nessa receita e ela foi pulada por causa da sua alergia\n', receita, '\nna verdade foi acidente a lista registrar como string mas serve pra coisas funcionarem no plural como egg ser parte de eggs. a receita era essa: id', placar.at[contador_indice, 'prato_id'].item(), '\n')
                placar.drop(contador_indice, inplace = True)
            contador_indice += 1


    if imprimir_metricas:
        print(f'{time.perf_counter() - inicio}s: FILTROS FINAIS EXECUTADOS E ORGANIZAÇÃO DA LISTA FINAL DE RESPOSTAS PREPARADA. PROCESSO FINALIZADO')
    return placar.head(limite)

def obter_recomendacoes(id: int = 0, k: int = 3, limite: int = 50, valorizacao_de_frequencia: float = 0.1, conexao: sqlite3.Connection | None = None, raw_receitas: DataFrame = DataFrame(), minimo_de_avaliacoes_pro_mesmo_prato_pra_nao_desconsiderar: int = 3, imprimir_metricas: bool = False, minimo_de_receitas_registradas_pra_nao_usar_as_do_onboarding: int = 5):
    if conexao is None:
        return None
    lista: DataFrame = (pd.read_sql("SELECT * FROM myapp_perfilusuario", con=conexao))
    lista_receitas: DataFrame = pd.read_sql("SELECT * FROM myapp_prato", con=conexao)
    interacoes: DataFrame = pd.read_sql("SELECT * FROM myapp_interacao", con=conexao)
    interacoes_por_id_de_usuario: DataFrame = interacoes.groupby('usuario_id')['prato_id'].apply(list)
    notas_por_id_de_usuario: DataFrame = interacoes.groupby('usuario_id')['nota'].apply(list)
    interacoes = interacoes.set_index('id')
    lista['items'] = lista.apply(lambda linha: interacoes_por_id_de_usuario.get(linha['usuario_id'], []), axis=1)
    lista['ratings'] = lista.apply(lambda linha: notas_por_id_de_usuario.get(linha['usuario_id'], []), axis=1)
    lista = lista.set_index('usuario_id')
    lista_escolhas_onboarding: DataFrame = pd.read_sql("SELECT * FROM myapp_onboardingprato", con=conexao)

    try:
        alergias = pd.read_sql("SELECT * FROM myapp_perfilusuario_alergias", con=conexao).groupby('perfilusuario_id')['alergia_id'].apply(list)[(lista.at[id, 'id'])]
    except (KeyError):
        alergias = []

    alergias_dict: dict = pd.read_sql("SELECT * FROM myapp_alergia", con=conexao).set_index('id').to_dict()['nome']

    return _obter_recomendacoes(
        alergias=alergias, lista=lista, lista_receitas=lista_receitas, interacoes=interacoes, lista_escolhas_onboarding=lista_escolhas_onboarding,
        alergias_dict=alergias_dict,
        id = id,
        k = k,
        limite=limite,
        valorizacao_de_frequencia=valorizacao_de_frequencia,
        raw_receitas=raw_receitas,
        minimo_de_avaliacoes_pro_mesmo_prato_pra_nao_desconsiderar=minimo_de_avaliacoes_pro_mesmo_prato_pra_nao_desconsiderar,
        minimo_de_receitas_registradas_pra_nao_usar_as_do_onboarding=minimo_de_receitas_registradas_pra_nao_usar_as_do_onboarding,
        imprimir_metricas=imprimir_metricas
    )
#descomentar pra testar com todos os usuarios que existem
#verificados = pd.read_sql("SELECT * FROM myapp_perfilusuario", con=conexao).set_index('usuario_id')
#print(verificados)
#verificados = [16]
#if __name__ == "__main__":
if False:
    verificados = [33]

    for usuario in verificados:
        print(
            f"\nid:{usuario}\n",
            obter_recomendacoes(
                id=usuario,
                k=100,
                limite=3,
                valorizacao_de_frequencia=0.2,
                conexao=sqlite3.connect("backend/PratoMatch/db.sqlite3"),
                raw_receitas=pd.read_csv("backend/dataset/RAW_recipes.csv").set_index("id"),
                minimo_de_avaliacoes_pro_mesmo_prato_pra_nao_desconsiderar=1,
                imprimir_metricas=True,
                minimo_de_receitas_registradas_pra_nao_usar_as_do_onboarding=5,
            ),
        )

def recall_arroba_n(k: int = 3, n: int = 20, rodadas: int = 3, minimo_receitas_por_usuario_teste: int = 10, receitas_previstas: int = 2,  valorizacao_de_frequencia: float = 0.1, conexao: sqlite3.Connection | None = None, raw_receitas: DataFrame = DataFrame(), imprimir_metricas: bool = False) -> float:
    if conexao is None:
        return None
    
    lista: DataFrame = (pd.read_sql("SELECT * FROM myapp_perfilusuario", con=conexao))
    lista_receitas: DataFrame = pd.read_sql("SELECT * FROM myapp_prato", con=conexao)
    interacoes: DataFrame = pd.read_sql("SELECT * FROM myapp_interacao", con=conexao)
    interacoes_por_id_de_usuario: DataFrame = interacoes.groupby('usuario_id')['prato_id'].apply(list)
    notas_por_id_de_usuario: DataFrame = interacoes.groupby('usuario_id')['nota'].apply(list)
    interacoes = interacoes.set_index('id')
    lista['items'] = lista.apply(lambda linha: interacoes_por_id_de_usuario.get(linha['usuario_id'], []), axis=1)
    lista['ratings'] = lista.apply(lambda linha: notas_por_id_de_usuario.get(linha['usuario_id'], []), axis=1)
    lista = lista.set_index('usuario_id')
    lista_escolhas_onboarding: DataFrame = pd.read_sql("SELECT * FROM myapp_onboardingprato", con=conexao)

    por_usuario = interacoes.groupby('usuario_id')['prato_id'].apply(list)
    elegiveis = por_usuario[por_usuario.apply(len) > minimo_receitas_por_usuario_teste].index.to_list()
    if len(elegiveis) == 0:
        return None
    total = 0
    ids = random.sample(elegiveis, rodadas)
    rodadas_completas = 0
    for id in ids:
        pratos = lista.loc[id]['items'].copy()
        notas = lista.loc[id]['ratings'].copy()
        tpratos = []
        tnotas = []

        for _ in range(receitas_previstas):
            r = random.randrange(len(pratos))
            tpratos.append(pratos.pop(r))
            tnotas.append(notas.pop(r))
        lista.at[id, 'items'] = pratos
        lista.at[id, 'ratings'] = notas
        dict_testes = dict(zip(tpratos, tnotas))

        alergias = []

        alergias_dict: dict = pd.read_sql("SELECT * FROM myapp_alergia", con=conexao).set_index('id').to_dict()['nome']

        resultado_encontrado = _obter_recomendacoes(
            alergias=alergias, lista=lista, lista_receitas=lista_receitas, interacoes=interacoes, lista_escolhas_onboarding=lista_escolhas_onboarding,
            alergias_dict=alergias_dict,
            id = id,
            k = k,
            limite=9999999,
            valorizacao_de_frequencia=0.0,
            raw_receitas=raw_receitas,
            minimo_de_avaliacoes_pro_mesmo_prato_pra_nao_desconsiderar=1,
            minimo_de_receitas_registradas_pra_nao_usar_as_do_onboarding=1,
            imprimir_metricas=imprimir_metricas
        )
        completo = resultado_encontrado.set_index('prato_id').index
        cortado = resultado_encontrado.head(min(n, len(resultado_encontrado))).set_index('prato_id').index

        achado = 0
        descontado = 0
        for prato in tpratos:
            if not prato in completo:
                descontado += 1
            elif prato in cortado:
                achado += 1
            (lista.at[id, 'items']).append(prato)
            lista.at[id, 'ratings'].append(dict_testes[prato])
        if not descontado == len(tpratos):
            total += (achado/(receitas_previstas - descontado))
            rodadas_completas += 1
    return total / rodadas_completas if rodadas_completas != 0 else None




#descomentar pra testar com todos os usuarios que existem
#verificados = pd.read_sql("SELECT * FROM myapp_perfilusuario", con=conexao).set_index('usuario_id')
#print(verificados)
#verificados = [16]
#if __name__ == "__main__":
if False:
    verificados = [33]

    for usuario in verificados:
        print(
            f"\nid:{usuario}\n",
            obter_recomendacoes(
                id=usuario,
                k=100,
                limite=3,
                valorizacao_de_frequencia=0.2,
                conexao=sqlite3.connect("backend/PratoMatch/db.sqlite3"),
                raw_receitas=pd.read_csv("backend/dataset/RAW_recipes.csv").set_index("id"),
                minimo_de_avaliacoes_pro_mesmo_prato_pra_nao_desconsiderar=1,
                imprimir_metricas=True,
                minimo_de_receitas_registradas_pra_nao_usar_as_do_onboarding=5,
            ),
        )

#lista_escolhas_onboarding: DataFrame = pd.read_sql("SELECT * FROM myapp_onboardingprato", con=conexao)
#lista_escolhas_onboarding['prato_id'] = [1, 2, 3, 1, 2, 3]
#lista_escolhas_onboarding['perfil_id'] = [1, 1, 1, 2, 2, 2]
#escolhas = (lista_escolhas_onboarding.groupby('perfil_id')['prato_id'].apply(list))
#print(escolhas.loc[2])
#myapp_alergia
#myapp_categoria
#myapp_ingrediente
#myapp_prato
#myapp_perfilusuario_alergias
#myapp_perfilusuario_categorias_preferidas
#myapp_perfilusuario_preferencias
#myapp_interacao


#isso daq é oq importa pro views
from functools import lru_cache #guarda o cache pra n precisar ler o csv toda vez, mt mais rapido
from pathlib import Path 
from django.db import connection

CAMINHO_RAW = Path(__file__).resolve().parents[1] / "dataset" / "RAW_recipes.csv"

#vai deixar guardado no cache apenas 1 resultado
@lru_cache(maxsize=1)
def _raw_receitas():
    return pd.read_csv(CAMINHO_RAW).set_index("id")


#chama a funçaõ principal de reocmendação, recomendar_para é a função chamadao pelo VIEWS do Django
def recomendar_para(usuario_id: int, limite: int = 60, imprimir: bool = False):
    #connection.ensure_connection()
    resultado: pd.DataFrame = obter_recomendacoes(
        id=usuario_id,
        k=100,
        limite=limite,
        valorizacao_de_frequencia=0.2,
        #conexao=connection.connection,  
        conexao=sqlite3.connect("backend/PratoMatch/db.sqlite3"),
        raw_receitas=_raw_receitas(),
        minimo_de_avaliacoes_pro_mesmo_prato_pra_nao_desconsiderar=1,
    )

    if imprimir:
        pratos = pd.read_sql(
            "SELECT * FROM myapp_prato",
            connection.connection
            #sqlite3.connect("backend/PratoMatch/db.sqlite3")
            ).set_index('id')
        for indice, linha in resultado.iterrows():
            print(f'\n{pratos.loc[int(linha['prato_id'])]}')

    return resultado

if __name__ == '__main__':
    #recomendar_para(33, imprimir=False)
    print(recall_arroba_n(conexao=sqlite3.connect("backend/PratoMatch/db.sqlite3"), raw_receitas=_raw_receitas()))