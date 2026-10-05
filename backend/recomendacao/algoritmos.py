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
import numpy as np

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

#NA VERDADE AGORA ISSO SE CHAMA PEARSON
# (as funções do k-NN abaixo ficam INTOCADAS e agora sem uso, só pra você poder comparar depois)
def calcular_similaridade_cosseno(lista_1: list[float], idxlista_1: list[int], lista_2: list[float], idxlista_2: list[int], min: int = 3) -> float:
    lista_1_comum: list[float] = []
    lista_2_comum: list[float] = []
    if idxlista_1 is None:
        return -1.0
    mapa2 = {idx:nota for idx, nota in zip(idxlista_2, lista_2)}
 
    for idx, nota in zip(idxlista_1, lista_1):
        if idx in mapa2:
            lista_1_comum.append(nota)
            lista_2_comum.append(mapa2[idx])
    if len(lista_1_comum) < min:
        return 0.0
 
    tamanho = len(lista_1_comum)
    media1 = sum(lista_1_comum)/tamanho
    media2 = sum(lista_2_comum)/tamanho
    lista_1_comum = [n - media1 for n in lista_1_comum]
    lista_2_comum = [n - media2 for n in lista_2_comum]
 
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
    try:
        usuario1 = lista.loc[id_usuario_1]
        usuario2 = lista.loc[id_usuario_2]
    except (KeyError):
        return 0.0
 
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
        similaridade: float = id_similaridade_cosseno(id, id2, lista, min)
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
 
 
# NOVO: treino do SVD (estilo Funk). previsão = mu + bu[u] + bi[i] + P[u] . Q[i]
def treinar_svd(usuarios, pratos, notas, k: int = 30, epocas: int = 10, lr: float = 0.005, reg: float = 0.02, reg_bi: float = 0.1, seed: int = 0, imprimir: bool = True) -> dict:
    rng = np.random.default_rng(seed)
    # np.unique devolve os ids ordenados e a posição de cada id em cada avaliação (return_inverse)
    ids_u, u_idx = np.unique(np.asarray(usuarios), return_inverse=True)
    ids_p, p_idx = np.unique(np.asarray(pratos), return_inverse=True)
    r = np.asarray(notas, dtype=float)
 
    mu = r.mean()
    bu = np.zeros(len(ids_u))
    bi = np.zeros(len(ids_p))
    P = rng.normal(0, 0.1, (len(ids_u), k))
    Q = rng.normal(0, 0.1, (len(ids_p), k))
    contagem = np.bincount(p_idx, minlength=len(ids_p)) #quantas avaliações cada receita tem
 
    for epoca in range(epocas):
        inicio = time.perf_counter()
        soma_erro2 = 0.0
        for n in rng.permutation(len(r)):
            u, i = u_idx[n], p_idx[n]
            erro = r[n] - (mu + bu[u] + bi[i] + P[u] @ Q[i])
            soma_erro2 += erro ** 2
            bu[u] += lr * (erro - reg * bu[u])
            bi[i] += lr * (erro - reg_bi * bi[i]) #reg_bi maior segura receita com poucas avaliações
            pu_antigo = P[u].copy() #o Q usa o P antigo
            P[u] += lr * (erro * Q[i] - reg * P[u])
            Q[i] += lr * (erro * pu_antigo - reg * Q[i])
        if imprimir:
            print(f'época {epoca + 1}/{epocas}: RMSE treino = {(soma_erro2 / len(r)) ** 0.5:.4f} ({time.perf_counter() - inicio:.1f}s)')
 
    return {'mu': mu, 'bu': bu, 'bi': bi, 'P': P, 'Q': Q, 'contagem': contagem, 'ids_u': ids_u, 'ids_p': ids_p,
            'pos_u': {int(x): n for n, x in enumerate(ids_u)}, 'pos_p': {int(x): n for n, x in enumerate(ids_p)}}
 
# NOVO: usuário que não estava no treino (ou que precisou do onboarding): ajusta só bu e p, com Q e bi fixos
def vetor_usuario_novo(modelo: dict, pratos: list, notas: list, passos: int = 200, lr: float = 0.02, reg: float = 0.02):
    pares = [(modelo['pos_p'][int(p)], float(n)) for p, n in zip(pratos, notas) if int(p) in modelo['pos_p']]
    bu = 0.0
    p = np.random.default_rng(0).normal(0, 0.1, modelo['Q'].shape[1])
    for _ in range(passos):
        for i, nota in pares:
            erro = nota - (modelo['mu'] + bu + modelo['bi'][i] + p @ modelo['Q'][i])
            bu += lr * (erro - reg * bu)
            p += lr * (erro * modelo['Q'][i] - reg * p)
    return bu, p
 
 
# MUDOU: ganhou os parâmetros modelo e minimo_de_avaliacoes_por_receita (no final). k, valorizacao_de_frequencia
# e minimo_de_avaliacoes_pro_mesmo_prato_pra_nao_desconsiderar continuam na assinatura mas o SVD não usa.
def _obter_recomendacoes(id: int = 0, k: int = 3, limite: int = 50, lista_trocas: DataFrame | None = None, valorizacao_de_frequencia: float = 0.1, alergias_dict: dict = {}, lista_escolhas_onboarding: DataFrame | None = None, lista: DataFrame | None = None, lista_receitas: DataFrame | None = None, interacoes: DataFrame | None = None, raw_receitas: DataFrame | None = None, alergias: list = [], minimo_de_avaliacoes_pro_mesmo_prato_pra_nao_desconsiderar: int = 3, imprimir_metricas: bool = False, minimo_de_receitas_registradas_pra_nao_usar_as_do_onboarding: int = 5, modelo: dict | None = None, minimo_de_avaliacoes_por_receita: int = 3):
 
    if imprimir_metricas:
        inicio = time.perf_counter()
        print(f"INICIO DO ALGORITMO DE BUSCA DE RECOMENDAÇÕES PARA USUÁRIO ID: {id}")
 
    if id not in lista.index:
        raise ValueError(f'Usuário com id {id} não encontrado ou não existe. ids na lista: {lista.index.to_list()}')
 
    usou_onboarding: bool = False # NOVO
    if len(lista.loc[id]['items']) < minimo_de_receitas_registradas_pra_nao_usar_as_do_onboarding:
        usou_onboarding = True # NOVO
        faltando: int = minimo_de_receitas_registradas_pra_nao_usar_as_do_onboarding - len(lista.loc[id]['items'])
 
        escolhas: list = (lista_escolhas_onboarding.groupby('perfil_id')['prato_id'].apply(list)).get(id, [])
        #print(escolhas)
        for n in escolhas:
            if faltando == 0:
                break
            #print('adicionando coisas da coisa la porque faltou')
            lista.at[id, 'items'].append(n)
            lista.loc[id, 'ratings'].append(5.0)
            faltando -= 1
        #print(lista.loc[id])
    
    receitas_usuario: list[int] = (lista.at[id, 'items'])
 
    # MUDOU: aqui ficava o k_nn + a agregação das notas dos vizinhos (receitas_novas, receitas_frequencia, receitas_valor...)
    # agora: pega o vetor do usuário e pontua todas as receitas de uma vez
    if modelo is None:
        modelo = _modelo()
    if id in modelo['pos_u'] and not usou_onboarding:
        bu_u = modelo['bu'][modelo['pos_u'][id]]
        p_u = modelo['P'][modelo['pos_u'][id]]
    else:
        bu_u, p_u = vetor_usuario_novo(modelo, receitas_usuario, lista.at[id, 'ratings'])
    scores = modelo['mu'] + bu_u + modelo['bi'] + modelo['Q'] @ p_u
    validos = modelo['contagem'] >= minimo_de_avaliacoes_por_receita # filtro de mínimo de avaliações
    validos &= ~np.isin(modelo['ids_p'], receitas_usuario) # tira o que o usuário já avaliou
    posicoes = np.flatnonzero(validos)
    posicoes = posicoes[np.argsort(-scores[posicoes])][:limite * 5] # candidatas, o filtro de alergia ainda vai cortar
    if imprimir_metricas:
        print(f'{time.perf_counter() - inicio}s: RECEITAS PONTUADAS PELO SVD')
    # mesmas colunas de antes. reset_index deixa o índice 0,1,2... na ordem do ranking (o loop de alergia depende disso)
    placar: DataFrame = DataFrame({
        'prato_id': modelo['ids_p'][posicoes],
        'nota_esperada': np.clip(scores[posicoes], 1.0, 5.0),
        'quantidade de avaliacoes': modelo['contagem'][posicoes],
        'valor interno de classificacao': scores[posicoes],
    }).reset_index(drop=True)
 
    if len(placar) == 0:
        ids_disponiveis = [
            int(prato_id)
            for prato_id in raw_receitas.index
            if int(prato_id) not in receitas_usuario
        ]
        quantidade = min(limite * 2, len(ids_disponiveis))
        sorteio = random.sample(ids_disponiveis, quantidade)
        placar = DataFrame({
            'prato_id': sorteio,
            'nota_esperada': 5.0,
            'quantidade de avaliacoes': 1,
            'valor interno de classificacao': 1.0,
        })
 
    filtro_ingredientes: list = [lista_trocas.loc[alergias_dict[chave]]['replaced'] if alergias_dict[chave] in lista_trocas.index else alergias_dict[chave] for chave in alergias]
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
 
# INTOCADA
def obter_recomendacoes(id: int = 0, k: int = 30, limite: int = 50, valorizacao_de_frequencia: float = 0.1, conexao: sqlite3.Connection | None = None, raw_receitas: DataFrame = DataFrame(), minimo_de_avaliacoes_pro_mesmo_prato_pra_nao_desconsiderar: int = 3, imprimir_metricas: bool = False, lista_trocas: DataFrame | None = None, minimo_de_receitas_registradas_pra_nao_usar_as_do_onboarding: int = 5):
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
    if lista_trocas is None:
        lista_trocas = pd.read_pickle(BASE_DIR / "dataset" / "ingr_map.pkl")
    lista_trocas.set_index('raw_ingr', inplace=True)
 
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
        imprimir_metricas=imprimir_metricas,
        lista_trocas=lista_trocas
    )
#descomentar pra testar com todos os usuarios que existem
#verificados = pd.read_sql("SELECT * FROM myapp_perfilusuario", con=conexao).set_index('usuario_id')
#print(verificados)
#verificados = [16]
 
# MUDOU: ganhou o parâmetro minimo_de_avaliacoes_por_receita. O laço único virou dois: um que ESCONDE as
# receitas de todos os usuários de teste, depois um treino único do SVD sem elas, e um que BUSCA e confere.
def recall_arroba_n(k: int = 2000, n: int = 500, rodadas: int = 3, minimo_receitas_por_usuario_teste: int = 55, receitas_previstas: int = 5, lista_trocas: DataFrame | None = None, conexao: sqlite3.Connection | None = None, raw_receitas: DataFrame = DataFrame(), imprimir_metricas: bool = False, minimo_de_avaliacoes_por_receita: int = 3) -> float:
    if conexao is None:
        return None
    
    lista: DataFrame = (pd.read_sql("SELECT * FROM myapp_perfilusuario", con=conexao))
    lista_receitas: DataFrame = pd.read_sql("SELECT * FROM myapp_prato", con=conexao)
    interacoes: DataFrame = pd.read_sql("SELECT * FROM myapp_interacao", con=conexao)
    interacoes_por_id_de_usuario: DataFrame = interacoes.groupby('usuario_id')['prato_id'].apply(list)
    notas_por_id_de_usuario: DataFrame = interacoes.groupby('usuario_id')['nota'].apply(list)
    interacoes = interacoes.set_index('id')
    if lista_trocas is None:
        lista_trocas = pd.read_pickle(BASE_DIR / "dataset" / "ingr_map.pkl")
    lista_trocas.set_index('raw_ingr', inplace=True)
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
    escondidos: dict = {} # NOVO: {id do usuário : {prato escondido : nota}}
 
    # PRIMEIRO LAÇO (só esconde)
    for id in ids:
        pratos = lista.loc[id]['items'].copy()
        notas = lista.loc[id]['ratings'].copy()
        tpratos = []
        tnotas = []
        #dict_testes = dict(zip(pratos, notas))
        #dict_testes = dict(sorted(dict_testes.items(), key = lambda item: item[1]))
        dict_testes: dict = pd.Series(data=lista.loc[id]['ratings'], index=lista.loc[id]['items']).sort_values().to_dict()
        for prato_id, nota in list(dict_testes.items())[-receitas_previstas:]:
            tpratos.append(prato_id)
            tnotas.append(nota)
            dict_testes.pop(prato_id)
        #print("id escolhido:", id)
        lista.at[id, 'items'] = list(dict_testes.keys())
        lista.at[id, 'ratings'] = list(dict_testes.values())
        #print('receitas a buscar:', tpratos, tnotas)
        escondidos[id] = dict(zip(tpratos, tnotas)) # NOVO
 
    # NOVO: treina UMA vez com tudo que sobrou (sem as receitas escondidas, senão o teste vaza)
    usuarios_treino = [u for u, itens in lista['items'].items() for _ in itens]
    pratos_treino = [p for itens in lista['items'] for p in itens]
    notas_treino = [nt for nts in lista['ratings'] for nt in nts]
    modelo_teste = treinar_svd(usuarios_treino, pratos_treino, notas_treino, epocas=5, imprimir=imprimir_metricas)
 
    # SEGUNDO LAÇO (busca, confere e devolve as receitas)
    for id in ids:
        dict_testes = escondidos[id] # MUDOU: antes era dict(zip(tpratos, tnotas)) feito no laço único
        tpratos = list(dict_testes.keys())
 
        alergias = []
 
        alergias_dict: dict = pd.read_sql("SELECT * FROM myapp_alergia", con=conexao).set_index('id').to_dict()['nome']
 
        resultado_encontrado = _obter_recomendacoes(
            alergias=alergias, lista=lista, lista_receitas=lista_receitas, interacoes=interacoes, lista_escolhas_onboarding=lista_escolhas_onboarding,
            alergias_dict=alergias_dict,
            id = id,
            k = k,
            limite=5000,
            valorizacao_de_frequencia=0.05,
            raw_receitas=raw_receitas,
            minimo_de_avaliacoes_pro_mesmo_prato_pra_nao_desconsiderar=25,
            minimo_de_receitas_registradas_pra_nao_usar_as_do_onboarding=1,
            imprimir_metricas=imprimir_metricas,
            lista_trocas=lista_trocas,
            modelo=modelo_teste, # NOVO
            minimo_de_avaliacoes_por_receita=minimo_de_avaliacoes_por_receita # NOVO
        )
        completo = resultado_encontrado.set_index('prato_id').index.to_list()
        cortado = resultado_encontrado.head(min(n, len(resultado_encontrado))).set_index('prato_id').index.to_list()
        #print(completo)
        #print(resultado_encontrado)
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
            #print('rodada completa resultado da rodada:', achado/(receitas_previstas - descontado))
    return total / rodadas_completas if rodadas_completas != 0 else None
 
 
#isso daq é oq importa pro views
from functools import lru_cache #guarda o cache pra n precisar ler o csv toda vez, mt mais rapido
from pathlib import Path 
from django.db import connection
 
CAMINHO_RAW = Path(__file__).resolve().parents[1] / "dataset" / "RAW_recipes.csv"
CAMINHO_BANCO = Path(__file__).resolve().parents[1] / "PratoMatch" / "db.sqlite3"
CAMINHO_MODELO = Path(__file__).resolve().parents[1] / "dataset" / "modelo_svd.npz" # NOVO
 
#vai deixar guardado no cache apenas 1 resultado
@lru_cache(maxsize=1)
def _raw_receitas():
    return pd.read_csv(CAMINHO_RAW).set_index("id")
 
# MUDOU: o treino NÃO acontece mais dentro da requisição (treinar leva vários minutos e travava o frontend).
# Treine uma vez, fora do servidor:  python recomendador.py --treinar
# Isso gera dataset/modelo_svd.npz. Usuário novo ou com avaliações novas NÃO precisa de retreino:
# vetor_usuario_novo ajusta o vetor dele na hora (é rápido). Retreine só de vez em quando (mudou hiperparâmetro, entrou muita gente/prato).
def treinar_e_salvar_modelo(epocas: int = 10) -> dict:
    conexao = sqlite3.connect(CAMINHO_BANCO, timeout=30)
    try:
        df = pd.read_sql("SELECT usuario_id, prato_id, nota FROM myapp_interacao", con=conexao)
    finally:
        conexao.close()
    modelo = treinar_svd(df['usuario_id'], df['prato_id'], df['nota'], epocas=epocas)
    # grava num arquivo temporário e troca no final, pra nunca deixar um .npz pela metade
    temporario = CAMINHO_MODELO.with_name(CAMINHO_MODELO.stem + "_tmp.npz")
    np.savez(temporario, **{chave: modelo[chave] for chave in ('mu', 'bu', 'bi', 'P', 'Q', 'contagem', 'ids_u', 'ids_p')})
    os.replace(temporario, CAMINHO_MODELO)
    return modelo

# só carrega do disco (e guarda em cache); se o arquivo não existe, avisa em vez de treinar no meio da requisição
@lru_cache(maxsize=1)
def _modelo():
    if not CAMINHO_MODELO.exists():
        raise FileNotFoundError(f"{CAMINHO_MODELO} não existe. Rode uma vez: python recomendador.py --treinar")
    with np.load(CAMINHO_MODELO) as arquivo:
        modelo = {chave: arquivo[chave] for chave in arquivo.files}
    modelo['mu'] = float(modelo['mu'])
    modelo['pos_u'] = {int(x): n for n, x in enumerate(modelo['ids_u'])}
    modelo['pos_p'] = {int(x): n for n, x in enumerate(modelo['ids_p'])}
    return modelo
 
 
#chama a funçaõ principal de reocmendação, recomendar_para é a função chamadao pelo VIEWS do Django
# INTOCADA
def recomendar_para(usuario_id: int, limite: int = 60, imprimir: bool = True):
    conexao = sqlite3.connect(CAMINHO_BANCO, timeout=30)
    try:
        conexao.execute("PRAGMA busy_timeout = 30000")
        conexao.execute("PRAGMA query_only = ON")
        resultado: pd.DataFrame = obter_recomendacoes(
            id=usuario_id,
            k=100,
            limite=limite,
            valorizacao_de_frequencia=0.2,
            conexao=conexao,
            raw_receitas=_raw_receitas(),
            minimo_de_avaliacoes_pro_mesmo_prato_pra_nao_desconsiderar=1,
        )
    finally:
        conexao.close()
 
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
    if '--treinar' in sys.argv:
        treinar_e_salvar_modelo()
        print(f'modelo salvo em {CAMINHO_MODELO}')
        sys.exit(0)
    #recomendar_para(33, imprimir=False)
    print("média de recall (500 rodadas)")
    print(recall_arroba_n(conexao=sqlite3.connect("backend/PratoMatch/db.sqlite3"), raw_receitas=_raw_receitas(), imprimir_metricas=False, rodadas=500, k = 15))