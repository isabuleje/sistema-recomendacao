def _normalizar(valor):
    return str(valor).strip().casefold()


def ordenar_por_categorias(ids, pratos_por_id, categorias, limite=None):
    """Prioriza pratos que correspondem às categorias escolhidas no onboarding."""
    categorias_normalizadas = {
        _normalizar(categoria)
        for categoria in (categorias or [])
        if _normalizar(categoria)
    }

    ids_unicos = list(dict.fromkeys(int(prato_id) for prato_id in ids))
    if not categorias_normalizadas:
        return ids_unicos[:limite] if limite is not None else ids_unicos

    correspondentes = []
    restantes = []

    for prato_id in ids_unicos:
        prato = pratos_por_id.get(prato_id, {})
        tags = {
            _normalizar(tag)
            for tag in prato.get("tags", [])
            if _normalizar(tag)
        }
        corresponde = any(
            categoria in tag or tag in categoria
            for categoria in categorias_normalizadas
            for tag in tags
        )
        (correspondentes if corresponde else restantes).append(prato_id)

    resultado = correspondentes + restantes
    return resultado[:limite] if limite is not None else resultado
