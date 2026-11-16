def cobertura_catalogo(recomendacoes, total_itens):
    if total_itens <= 0:
        return 0.0

    return len(set(recomendacoes)) / total_itens