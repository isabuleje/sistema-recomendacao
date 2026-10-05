# Avaliação offline (recall@n, HitRate@n, nDCG@n, AUC médio e baseline aleatório).
# NÃO é importado pelo Django/views: só roda quando você executa este arquivo manualmente.
# Uso (na mesma pasta do recomendador):  python metricas_offline.py
import random
import sqlite3

import numpy as np
import pandas as pd
from pandas.core.frame import DataFrame

from algoritmos import BASE_DIR, _obter_recomendacoes, _raw_receitas, treinar_svd


# MUDOU: ganhou o parâmetro minimo_de_avaliacoes_por_receita. O laço único virou dois: um que ESCONDE as
# receitas de todos os usuários de teste, depois um treino único do SVD sem elas, e um que BUSCA e confere.
# NOVO: ganhou retornar_todas. Com False (padrão) devolve só o recall, como antes. Com True devolve um dict com
# recall, hit (HitRate@n), ndcg (nDCG@n), auc (percentil médio no ranking: 0.5 = aleatório, 1.0 = perfeito)
# e aleatorio (recall esperado de um ranking aleatório, pra comparar com o recall).
def recall_arroba_n(k: int = 2000, n: int = 500, rodadas: int = 3, minimo_receitas_por_usuario_teste: int = 55, receitas_previstas: int = 5, lista_trocas: DataFrame | None = None, conexao: sqlite3.Connection | None = None, raw_receitas: DataFrame = DataFrame(), imprimir_metricas: bool = False, minimo_de_avaliacoes_por_receita: int = 3, retornar_todas: bool = False):
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
    # NOVO: soma das métricas de todas as rodadas (o recall é o mesmo de antes)
    soma = {'recall': 0.0, 'hit': 0.0, 'ndcg': 0.0, 'auc': 0.0, 'aleatorio': 0.0}
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
        cortado = completo[:min(n, len(completo))]
        posicao = {p: i for i, p in enumerate(completo)} # NOVO: posição de cada prato no ranking (0 = primeiro)
        #print(completo)
        #print(resultado_encontrado)
        achado = 0
        descontado = 0
        dcg = 0.0 # NOVO
        percentis = [] # NOVO
        for prato in tpratos:
            if prato not in posicao:
                descontado += 1
            else:
                percentis.append(1 - posicao[prato] / len(completo)) # NOVO: 1.0 = topo do ranking, ~0 = fim
                if posicao[prato] < len(cortado):
                    achado += 1
                    dcg += 1 / np.log2(posicao[prato] + 2) # NOVO
            (lista.at[id, 'items']).append(prato)
            lista.at[id, 'ratings'].append(dict_testes[prato])
        if not descontado == len(tpratos):
            avaliaveis = receitas_previstas - descontado
            idcg = sum(1 / np.log2(i + 2) for i in range(min(avaliaveis, len(cortado)))) # NOVO: melhor DCG possível
            soma['recall'] += achado / avaliaveis
            soma['hit'] += 1.0 if achado > 0 else 0.0
            soma['ndcg'] += dcg / idcg if idcg > 0 else 0.0
            soma['auc'] += float(np.mean(percentis))
            soma['aleatorio'] += len(cortado) / len(completo)
            rodadas_completas += 1
            #print('rodada completa resultado da rodada:', achado/avaliaveis)

    if rodadas_completas == 0:
        return None
    medias = {nome: valor / rodadas_completas for nome, valor in soma.items()}
    return medias if retornar_todas else medias['recall']


if __name__ == '__main__':
    print("médias das métricas (500 rodadas)")
    resultados = recall_arroba_n(conexao=sqlite3.connect("backend/PratoMatch/db.sqlite3"), raw_receitas=_raw_receitas(), imprimir_metricas=False, rodadas=500, k = 15, retornar_todas=True)
    if resultados is None:
        print("nenhuma rodada completa")
    else:
        for nome, valor in resultados.items():
            print(f'{nome}: {valor:.4f}')