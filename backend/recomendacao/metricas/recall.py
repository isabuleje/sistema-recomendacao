def recall_at_k(recomendados, relevantes, k=10):
    if k < 1:
        raise ValueError("k deve ser maior ou igual a 1")

    relevantes = set(relevantes)
    acertos = len(set(recomendados[:k]) & relevantes)

    return acertos / len(relevantes) if relevantes else 0.0