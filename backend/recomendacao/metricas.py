"""Metricas offline para avaliar rankings de recomendacoes."""

from collections.abc import Hashable, Iterable, Mapping
from typing import Any


def mrr_at_k(
    rankings_por_usuario: Mapping[Hashable, Iterable[Hashable]],
    itens_relevantes_por_usuario: Mapping[Hashable, Iterable[Hashable]],
    k: int = 5,
    incluir_usuarios_sem_ground_truth: bool = False,
) -> float:
    """Calcula Mean Reciprocal Rank (MRR@k) para rankings por usuario.

    A populacao avaliada e, por padrao, a intersecao entre os usuarios com
    ranking e os usuarios com ground truth. Quando a opcao e habilitada,
    usuarios sem ground truth recebem score zero e entram na media.
    Duplicatas sao removidas preservando a primeira ocorrencia.
    """
    if k < 1:
        raise ValueError("k deve ser maior ou igual a 1")

    usuarios = set(rankings_por_usuario) & set(itens_relevantes_por_usuario)
    if incluir_usuarios_sem_ground_truth:
        usuarios = set(rankings_por_usuario)

    if not usuarios:
        return 0.0

    soma_reciprocos = 0.0
    for usuario in usuarios:
        relevantes = set(itens_relevantes_por_usuario.get(usuario, ()))
        vistos: set[Hashable] = set()

        for item in rankings_por_usuario.get(usuario, ()):
            if item in vistos:
                continue
            vistos.add(item)
            if len(vistos) > k:
                break
            if item in relevantes:
                soma_reciprocos += 1.0 / len(vistos)
                break

    return soma_reciprocos / len(usuarios)


def ground_truth_por_nota(
    interacoes: Iterable[Mapping[str, Any]],
    nota_minima: float = 4,
    usuario_chave: str = "user_id",
    item_chave: str = "recipe_id",
    nota_chave: str = "rating",
) -> dict[Hashable, set[Hashable]]:
    """Cria ground truth por usuario a partir de interacoes avaliadas."""
    relevantes: dict[Hashable, set[Hashable]] = {}
    for interacao in interacoes:
        if interacao[nota_chave] >= nota_minima:
            usuario = interacao[usuario_chave]
            relevantes.setdefault(usuario, set()).add(interacao[item_chave])
    return relevantes