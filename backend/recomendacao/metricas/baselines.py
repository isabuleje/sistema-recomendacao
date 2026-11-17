import numpy as np

def ranking_aleatorio(ids_catalogo, conhecidas, rng, k):
    candidatos = [
        int(prato_id)
        for prato_id in ids_catalogo
        if int(prato_id) not in conhecidas
    ]
    rng.shuffle(candidatos)
    return candidatos[:k]


def ranking_popular(treino, conhecidas, k):
    popularidade = (
        treino.groupby("prato_id")["nota"]
        .agg(media="mean", quantidade="count")
        .sort_values(["media", "quantidade"], ascending=False)
    )
    return [
        int(prato_id)
        for prato_id in popularidade.index
        if int(prato_id) not in conhecidas
    ][:k]


def avaliar_rankings(rankings, relevantes, k, metricas):
    resultados = {}
    for nome, rankings_por_usuario in rankings.items():
        valores = {
            metrica: [
                funcao(rankings_por_usuario.get(usuario, []), relevantes[usuario], k,)
                for usuario in relevantes
            ]
            for metrica, funcao in metricas.items()
        }
        resultados[nome] = {
            metrica: float(np.mean(valores[metrica]))
            for metrica in metricas
        }
    return resultados
