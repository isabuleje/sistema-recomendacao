from math import log2

def ndcg_at_k(recomendados, relevantes, k=10):
    if k < 1:
        raise ValueError("k deve ser maior ou igual a 1")

    recomendados = list(recomendados)[:k]
    relevantes = set(relevantes)

    dcg = sum(
        1 / log2(posicao + 2)
        for posicao, item in enumerate(recomendados)
        if item in relevantes
    )

    quantidade_ideal = min(len(relevantes), k)
    idcg = sum(
        1 / log2(posicao + 2)
        for posicao in range(quantidade_ideal)
    )

    return dcg / idcg if idcg else 0.0