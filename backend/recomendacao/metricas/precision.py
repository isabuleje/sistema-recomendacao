def precision_at_k(recomendados, relevantes, k=10):
    if k < 1:
        raise ValueError("k deve ser maior ou igual a 1")

    acertos = len(set(recomendados[:k]) & set(relevantes))
    return acertos / k