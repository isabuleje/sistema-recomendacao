def _texto(lista, limite=4):
    itens = sorted(dict.fromkeys(item.strip() for item in lista if item and item.strip()))
    if not itens:
        return ""
    if len(itens) == 1:
        return itens[0]
    return ", ".join(itens[:limite])


def _formatar_tempo(segundos):
    segundos = max(0, int(segundos or 0))
    if segundos < 60:
        return f"{segundos} segundo{'s' if segundos != 1 else ''}"
    minutos = segundos // 60
    if minutos < 60:
        return f"{minutos} minuto{'s' if minutos != 1 else ''}"
    horas = minutos // 60
    minutos_restantes = minutos % 60
    if minutos_restantes:
        return f"{horas} h e {minutos_restantes} min"
    return f"{horas} h"


def _normalizar_interacoes(interacoes, pratos_por_id):
    normalizadas = []
    for interacao in interacoes or []:
        if isinstance(interacao, dict):
            prato_id = interacao.get("prato_id") or interacao.get("prato")
            nota = interacao.get("nota", 0)
            tempo = interacao.get("tempo_visualizado", 0)
        else:
            prato_id = getattr(interacao, "prato_id", None)
            nota = getattr(interacao, "nota", 0)
            tempo = getattr(interacao, "tempo_visualizado", 0)

        try:
            prato_id = int(prato_id)
        except (TypeError, ValueError):
            continue

        normalizadas.append({
            "prato_id": prato_id,
            "nota": int(nota or 0),
            "tempo": int(tempo or 0),
            "prato": pratos_por_id.get(prato_id, {}),
        })
    return normalizadas


def explicar_recomendacao(
    prato,
    pratos_por_id,
    categorias=None,
    historico_ids=None,
    interacoes=None,
    pratos_onboarding_ids=None,
):
    tags = {
        str(tag).strip().casefold()
        for tag in prato.get("tags", [])
        if str(tag).strip()
    }
    ingredientes_prato = {
        str(item).strip().casefold(): str(item).strip()
        for item in prato.get("ingredientes", [])
        if str(item).strip()
    }

    motivos = []

    categorias_encontradas = []
    for categoria in categorias or []:
        nome_categoria = str(categoria).strip()
        categoria_normalizada = nome_categoria.casefold()
        if not nome_categoria:
            continue
        if any(
            categoria_normalizada in tag or tag in categoria_normalizada
            for tag in tags
        ):
            categorias_encontradas.append(nome_categoria)

    if categorias_encontradas:
        texto_categorias = _texto(categorias_encontradas)
        motivos.append(
            f"Combina com "
            f"{'a categoria selecionada' if len(categorias_encontradas) == 1 else 'as categorias selecionadas'} "
            f"no onboarding: {texto_categorias}."
        )

    ids_onboarding = {
        int(prato_id)
        for prato_id in (pratos_onboarding_ids or [])
        if str(prato_id).isdigit()
    }
    ingredientes_onboarding = set()
    nomes_onboarding = []
    for prato_id in ids_onboarding:
        prato_onboarding = pratos_por_id.get(prato_id, {})
        ingredientes_onboarding.update(
            str(item).strip().casefold()
            for item in prato_onboarding.get("ingredientes", [])
            if str(item).strip()
        )
        nome = str(prato_onboarding.get("nome", "")).strip()
        if nome:
            nomes_onboarding.append(nome)

    comuns_onboarding = [
        ingredientes_prato[item]
        for item in ingredientes_prato
        if item in ingredientes_onboarding
    ]
    if comuns_onboarding:
        texto_onboarding = _texto(comuns_onboarding)
        motivos.append(
            f"Você marcou pratos de interesse no onboarding que compartilham "
            f"{texto_onboarding} com esta recomendação."
        )

    normalizadas = _normalizar_interacoes(interacoes, pratos_por_id)

    bem_avaliados = [
        interacao
        for interacao in normalizadas
        if interacao["nota"] >= 4
    ]
    ingredientes_bem_avaliados = set()
    nomes_bem_avaliados = []
    for interacao in bem_avaliados:
        prato_historico = interacao["prato"]
        ingredientes_bem_avaliados.update(
            str(item).strip().casefold()
            for item in prato_historico.get("ingredientes", [])
            if str(item).strip()
        )
        nome = str(prato_historico.get("nome", "")).strip()
        if nome:
            nomes_bem_avaliados.append(nome)

    comuns_bem_avaliados = [
        ingredientes_prato[item]
        for item in ingredientes_prato
        if item in ingredientes_bem_avaliados
    ]
    if comuns_bem_avaliados:
        texto_ingredientes = _texto(comuns_bem_avaliados)
        texto_pratos = _texto(nomes_bem_avaliados, limite=3)
        referencia = f", como {texto_pratos}," if texto_pratos else ""
        motivos.append(
            f"Você deu notas altas a pratos{referencia} que também usam "
            f"{texto_ingredientes}. "
        )

    interacoes_relacionadas = []
    ingredientes_tempo = set()
    tempo_total = 0
    for interacao in normalizadas:
        prato_historico = interacao["prato"]
        ingredientes_historico = {
            str(item).strip().casefold()
            for item in prato_historico.get("ingredientes", [])
            if str(item).strip()
        }
        comuns = set(ingredientes_prato) & ingredientes_historico
        if comuns and interacao["tempo"] > 0:
            interacoes_relacionadas.append((interacao, comuns))
            ingredientes_tempo.update(comuns)
            tempo_total += interacao["tempo"]

    if interacoes_relacionadas:
        nomes_tempo = [
            str(interacao["prato"].get("nome", "")).strip()
            for interacao, _ in sorted(
                interacoes_relacionadas,
                key=lambda item: item[0]["tempo"],
                reverse=True,
            )
            if str(interacao["prato"].get("nome", "")).strip()
        ]
        texto_tempo = _formatar_tempo(tempo_total)
        texto_ingredientes = _texto(
            [ingredientes_prato[item] for item in ingredientes_tempo]
        )
        texto_pratos = _texto(nomes_tempo, limite=3)
        referencia = f" ao visualizar {texto_pratos}" if texto_pratos else ""
        motivos.append(
            f"Você acumulou {texto_tempo}{referencia}, em páginas relacionadas "
            f"a {texto_ingredientes}, ingredientes presentes nesta recomendação."
        )

    if not motivos:
        if historico_ids:
            motivos.append(
                "Esta recomendação tem uma boa correspondência TF-IDF "
                "com os ingredientes dos seus pratos bem avaliados."
            )
        else:
            motivos.append(
                "Esta recomendação foi criada a partir das preferências e "
                "categorias informadas no onboarding."
            )

    return " ".join(motivos).strip()