"""Avaliação offline do recomendador PratoMatch com MRR@k (protocolo leave-out).

Protocolo
---------
1. Sorteia `usuarios_teste` usuários com avaliações relevantes suficientes.
2. Para cada um, esconde `n_escondidos` pratos relevantes (nota >= nota_relevante).
3. Roda o recomendador (com os mesmos parâmetros de produção) e pega o top-k.
4. O ground truth do usuário é o conjunto de pratos escondidos.
5. MRR@k = média de 1 / posição do primeiro prato escondido no top-k (0 se ausente).

Os baselines (popularidade e aleatório) usam exatamente os mesmos usuários e
os mesmos pratos escondidos, então a comparação é justa.
"""

import heapq
import random
import sqlite3
import statistics
import time
from collections import Counter

import pandas as pd
from pandas import DataFrame

from metricas import mrr_at_k  
from algoritmos import _obter_recomendacoes 


def _carregar_dados(conexao: sqlite3.Connection) -> dict:
    """Mesmo carregamento do recall_arroba_n, num lugar só."""
    lista: DataFrame = pd.read_sql("SELECT * FROM myapp_perfilusuario", con=conexao)
    lista_receitas: DataFrame = pd.read_sql("SELECT * FROM myapp_prato", con=conexao)
    interacoes: DataFrame = pd.read_sql("SELECT * FROM myapp_interacao", con=conexao)
    pratos_por_usuario = interacoes.groupby('usuario_id')['prato_id'].apply(list)
    notas_por_usuario = interacoes.groupby('usuario_id')['nota'].apply(list)
    interacoes = interacoes.set_index('id')
    lista['items'] = lista.apply(lambda l: pratos_por_usuario.get(l['usuario_id'], []), axis=1)
    lista['ratings'] = lista.apply(lambda l: notas_por_usuario.get(l['usuario_id'], []), axis=1)
    lista = lista.set_index('usuario_id')
    return {
        'lista': lista,
        'lista_receitas': lista_receitas,
        'interacoes': interacoes,
        'onboarding': pd.read_sql("SELECT * FROM myapp_onboardingprato", con=conexao),
        'alergias_dict': pd.read_sql("SELECT * FROM myapp_alergia", con=conexao).set_index('id').to_dict()['nome'],
    }


def _relevantes(pratos: list, notas: list, nota_relevante: float) -> list:
    """Pratos únicos com nota >= nota_relevante, na ordem em que aparecem."""
    vistos: set = set()
    saida: list = []
    for prato, nota in zip(pratos, notas):
        if nota >= nota_relevante and prato not in vistos:
            vistos.add(prato)
            saida.append(prato)
    return saida


def _ranking_popularidade(popularidade: Counter, excluir: set, descontar: set, k: int) -> list:
    """Top-k pratos mais populares, sem contar o próprio usuário e sem os pratos que ele já tem.

    Desempate determinístico por prato_id.
    """
    candidatos = (
        (-(contagem - (1 if prato in descontar else 0)), prato)
        for prato, contagem in popularidade.items()
        if prato not in excluir
    )
    return [prato for _, prato in heapq.nsmallest(k, candidatos)]


def mrr_arroba_k(
    k: int = 5,
    usuarios_teste: int = 100,
    minimo_receitas_restantes: int = 5,
    nota_relevante: float = 4.0,
    n_escondidos: int = 1,
    k_vizinhos: int = 100,
    valorizacao_de_frequencia: float = 0.2,
    minimo_avaliacoes_em_comum: int = 1,
    seed: int = 42,
    conexao: sqlite3.Connection | None = None,
    raw_receitas: DataFrame | None = None,
    dados: dict | None = None,
    imprimir_progresso: bool = True,
) -> dict:
    """Calcula MRR@k do recomendador (e de dois baselines) com o protocolo leave-out.

    Os defaults de k_vizinhos, valorizacao_de_frequencia e minimo_avaliacoes_em_comum
    espelham os usados em `recomendar_para`, para medir o sistema como ele roda em produção.
    """
    if dados is None:
        if conexao is None:
            raise ValueError("passe `conexao` ou `dados`")
        dados = _carregar_dados(conexao)
    if raw_receitas is None:
        raw_receitas = DataFrame()  # só é usado no filtro de alergias, que aqui fica desligado
    if n_escondidos < 1:
        raise ValueError("n_escondidos deve ser >= 1")

    lista: DataFrame = dados['lista']
    todos_pratos: list = dados['lista_receitas']['id'].tolist()

    rng = random.Random(seed)
    rng_base = random.Random(seed + 1)

    # popularidade global: quantos usuários avaliaram o prato como relevante
    popularidade: Counter = Counter()
    for u in lista.index:
        for prato in _relevantes(lista.at[u, 'items'], lista.at[u, 'ratings'], nota_relevante):
            popularidade[prato] += 1

    elegiveis = sorted(
        int(u) for u in lista.index
        if len(_relevantes(lista.at[u, 'items'], lista.at[u, 'ratings'], nota_relevante)) >= n_escondidos
        and len(set(lista.at[u, 'items'])) - n_escondidos >= minimo_receitas_restantes
    )
    if not elegiveis:
        raise ValueError("nenhum usuário elegível para o teste com esses parâmetros")
    ids = rng.sample(elegiveis, min(usuarios_teste, len(elegiveis)))

    rankings: dict = {}
    rankings_pop: dict = {}
    rankings_rand: dict = {}
    verdade: dict = {}
    inicio = time.perf_counter()

    for n_feitos, u in enumerate(ids, start=1):
        pratos_orig = lista.at[u, 'items']
        notas_orig = lista.at[u, 'ratings']
        relevantes = _relevantes(pratos_orig, notas_orig, nota_relevante)
        escondidos = set(rng.sample(relevantes, n_escondidos))

        # remove TODAS as ocorrências dos pratos escondidos (evita duplicata vazar o gabarito)
        restantes = [(p, n) for p, n in zip(pratos_orig, notas_orig) if p not in escondidos]
        lista.at[u, 'items'] = [p for p, _ in restantes]
        lista.at[u, 'ratings'] = [n for _, n in restantes]
        try:
            resultado = _obter_recomendacoes(
                id=u,
                k=k_vizinhos,
                limite=k,
                valorizacao_de_frequencia=valorizacao_de_frequencia,
                alergias=[],
                alergias_dict=dados['alergias_dict'],
                lista=lista,
                lista_receitas=dados['lista_receitas'],
                interacoes=dados['interacoes'],
                lista_escolhas_onboarding=dados['onboarding'],
                raw_receitas=raw_receitas,
                minimo_de_avaliacoes_pro_mesmo_prato_pra_nao_desconsiderar=minimo_avaliacoes_em_comum,
                minimo_de_receitas_registradas_pra_nao_usar_as_do_onboarding=1,
                permitir_fallback_aleatorio=False,
            )
        finally:
            # restaura SEMPRE o estado original do usuário, mesmo se der erro
            lista.at[u, 'items'] = pratos_orig
            lista.at[u, 'ratings'] = notas_orig

        ja_tem = {p for p, _ in restantes}
        rankings[u] = resultado['prato_id'].tolist()[:k]  # [] conta como 0 (usuário sem vizinhos)
        verdade[u] = escondidos
        rankings_pop[u] = _ranking_popularidade(popularidade, ja_tem, set(relevantes), k)
        candidatos = [p for p in todos_pratos if p not in ja_tem]
        rankings_rand[u] = rng_base.sample(candidatos, min(k, len(candidatos)))

        if imprimir_progresso and (n_feitos % 10 == 0 or n_feitos == len(ids)):
            print(f"[{n_feitos}/{len(ids)}] {time.perf_counter() - inicio:.1f}s")

    cobertos = {u: r for u, r in rankings.items() if r}
    acertos = sum(1 for u, r in rankings.items() if set(r) & verdade[u])
    return {
        'k': k,
        'seed': seed,
        'usuarios_avaliados': len(rankings),
        'cobertura': len(cobertos) / len(rankings),
        'mrr_at_k': mrr_at_k(rankings, verdade, k=k),
        'mrr_apenas_cobertos': mrr_at_k(cobertos, verdade, k=k) if cobertos else 0.0,
        'hit_rate_at_k': acertos / len(rankings),
        'mrr_popularidade': mrr_at_k(rankings_pop, verdade, k=k),
        'mrr_aleatorio': mrr_at_k(rankings_rand, verdade, k=k),
    }


def mrr_varias_seeds(seeds=range(1, 6), conexao: sqlite3.Connection | None = None, **kwargs) -> dict:
    """Repete a avaliação com várias seeds e devolve {métrica: (média, desvio)}."""
    dados = _carregar_dados(conexao)
    execucoes = [mrr_arroba_k(seed=s, dados=dados, **kwargs) for s in seeds]
    chaves = ['mrr_at_k', 'mrr_apenas_cobertos', 'hit_rate_at_k', 'cobertura', 'mrr_popularidade', 'mrr_aleatorio']
    resumo = {}
    for chave in chaves:
        valores = [e[chave] for e in execucoes]
        resumo[chave] = (statistics.mean(valores), statistics.stdev(valores) if len(valores) > 1 else 0.0)
    return resumo


if __name__ == '__main__':
    conexao = sqlite3.connect("backend/PratoMatch/db.sqlite3")

    # uma rodada rápida
    print(mrr_arroba_k(k=5, usuarios_teste=50, conexao=conexao))

    # para o trabalho: várias seeds, média ± desvio
    # for nome, (media, desvio) in mrr_varias_seeds(conexao=conexao, usuarios_teste=100).items():
    #     print(f"{nome}: {media:.4f} ± {desvio:.4f}")