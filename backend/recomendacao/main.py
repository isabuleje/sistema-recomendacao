from pathlib import Path
import pandas as pd
import ast

# Ler CSV e mostrar as receitas encontradas
BASE_DIR = Path(__file__).resolve().parent.parent

RECEITAS = pd.read_csv(BASE_DIR / "dataset" / "RAW_recipes.csv")
INTERACOES = pd.read_csv(
    BASE_DIR / "dataset" / "RAW_interactions.csv"
)


#Tags e ingredientes estão como string, então tem que converter para lista
RECEITAS["tags"] = RECEITAS["tags"].apply(
    lambda x: ast.literal_eval(x) if isinstance(x, str) else []
)

RECEITAS["ingredients"] = RECEITAS["ingredients"].apply(
    lambda x: ast.literal_eval(x) if isinstance(x, str) else []
)

# Tags que NÃO serão consideradas categorias
TAGS_IGNORAR = {
    "15-minutes-or-less",
    "30-minutes-or-less",
    "60-minutes-or-less",
    "4-hours-or-less",
    "1-day-or-more",

    "1-step",
    "2-steps-or-less",
    "3-steps-or-less",
    "4-steps-or-less",
    "5-ingredients-or-less",

    "course",
    "cuisine",
    "dietary",
    "equipment",
    "occasion",
    "preparation",
    "technique",
    "time-to-make",
    "main-ingredient",
    "number-of-servings",


    "bake",
    "baked",
    "baking",
    "broil",
    "deep-fry",
    "dehydrate",
    "grill",
    "grilling",
    "roast",
    "roasting",
    "steam",
    "steaming",
    "stove-top",
    "no-cook",

    "oven",
    "microwave",
    "mixer",
    "dehydrator",
    "food-processor-blender",
    "bread-machine",
    "crock-pot-slow-cooker",
    "pressure-cooker",
    "refrigerator",
    "smoker",
    "small-appliance",
    "april-fools-day",
    "birthday",
    "camping",
    "christmas",
    "chinese-new-year",
    "cinco-de-mayo",
    "dinner-party",
    "easter",
    "fathers-day",
    "halloween",
    "hanukkah",
    "independence-day",
    "labor-day",
    "mardi-gras-carnival",
    "memorial-day",
    "mothers-day",
    "new-years",
    "passover",
    "picnic",
    "potluck",
    "ramadan",
    "romantic",
    "st-patricks-day",
    "super-bowl",
    "superbowl",
    "thanksgiving",
    "valentines-day",
    "wedding",


    "beginner-cook",
    "college",
    "infant-baby-friendly",
    "kid-friendly",
    "toddler-friendly",
    "for-1-or-2",
    "for-large-groups",
    "for-large-groups-holiday-event",


    "easy",
    "inexpensive",
    "weeknight",
    "leftovers",
    "freezer",
    "freezer-friendly",
    "oamc-freezer-make-ahead",
    "unprocessed-freezer",

    "canning",
    "pressure-canning",
    "water-bath",
    "presentation",
    "garnishes",
    "served-cold",
    "served-hot",
    "to-go",
    "a1-sauce",
    

    # tags sus
    "Throw the ultimate fiesta with this sopaipillas recipe from Food.com.",
    "less_thansql:name_topics_of_recipegreater_than",
}


RECEITAS["categorias"] = RECEITAS["tags"].apply(
    lambda tags: [
        tag for tag in tags
        if tag not in TAGS_IGNORAR
    ]
)

def obter_categorias():

    categorias_unicas = sorted(
        {
            categoria.capitalize()
            for lista in RECEITAS["categorias"]
            for categoria in lista
            if isinstance(categoria, str)
            and categoria.strip()
        },
        key=str.lower
    )

    return categorias_unicas


def obter_ingredientes():

    ingredientes_unicos = sorted(
        {
            ingrediente.strip().capitalize()
            for lista in RECEITAS["ingredients"]
            for ingrediente in lista
            if isinstance(ingrediente, str)
            and ingrediente.strip()
            and not any(char.isdigit() for char in ingrediente)
        },
        key=str.lower
    )

    return ingredientes_unicos


#Antes do obter pratos, pq ele vem do RAW_interactions e nao do RAW_recipes
avaliacoes = (
    INTERACOES
    .groupby("recipe_id")["rating"]
    .agg(
        estrelas="mean",
        avaliacoes="count"
    )
    .reset_index()
)

df = RECEITAS.merge(
    avaliacoes,
    left_on="id",
    right_on="recipe_id",
    how="left"
)

#Obter pratos com limite ou ids específicos, e montar o dict de cada prato pq tava demorando horrores no frontend
def _montar_prato(prato):
    """Converte uma linha do DataFrame em dict — chamado só 1x por prato, no import."""
    prato_id = int(prato["id"]) if pd.notna(prato["id"]) else None

    steps = prato["steps"]
    if isinstance(steps, str):
        try:
            steps = ast.literal_eval(steps)
        except (ValueError, SyntaxError):
            steps = []
    if not isinstance(steps, list):
        steps = []

    return {
        "id": prato_id,
        "nome": str(prato["name"]).strip().capitalize() if pd.notna(prato["name"]) else "Prato sem nome",
        "descricao": str(prato["description"]).strip().capitalize() if pd.notna(prato["description"]) else "",
        "tempo_preparo": int(prato["minutes"]) if pd.notna(prato["minutes"]) else 0,
        "estrelas": round(float(prato["estrelas"]), 1) if pd.notna(prato["estrelas"]) else 0,
        "avaliacoes": int(prato["avaliacoes"]) if pd.notna(prato["avaliacoes"]) else 0,
        "tags": [t.capitalize() for t in prato["categorias"]] if isinstance(prato["categorias"], list) else [],
        "ingredientes": [i.capitalize() for i in prato["ingredients"]] if isinstance(prato["ingredients"], list) else [],
        "numero_ingredientes": int(prato["n_ingredients"]) if pd.notna(prato["n_ingredients"]) else 0,
        "numero_passos": int(prato["n_steps"]) if pd.notna(prato["n_steps"]) else 0,
        "passos": [p.capitalize() for p in steps],
    }


# Monta o índice UMA VEZ, no import do módulo — não a cada request
#ele tava fazendo o processo a cada resquest, agr vai super rapido
_PRATOS_POR_ID = {
    montado["id"]: montado
    for _, linha in df.iterrows()
    for montado in [_montar_prato(linha)]
    if montado["id"] is not None
}
_PRATOS_LISTA = list(_PRATOS_POR_ID.values())


def obter_pratos(limite=None, ids=None):
    if ids is not None:
        # lookup O(1) por id, sem varrer nada
        return [_PRATOS_POR_ID[i] for i in ids if i in _PRATOS_POR_ID]

    if limite is not None:
        return _PRATOS_LISTA[:limite]

    return _PRATOS_LISTA


def obter_pratos_onboarding(alergias=None, categorias=None, limite=24):
    """Retorna candidatos reais, seguros e variados para a terceira etapa."""
    alergias = {
        str(valor).strip().casefold()
        for valor in (alergias or [])
        if str(valor).strip()
    }
    categorias = {
        str(valor).strip().casefold()
        for valor in (categorias or [])
        if str(valor).strip()
    }

    candidatos = []
    for prato in _PRATOS_LISTA:
        ingredientes = {
            str(ingrediente).strip().casefold()
            for ingrediente in prato.get("ingredientes", [])
        }
        tags = {
            str(tag).strip().casefold()
            for tag in prato.get("tags", [])
        }

        if alergias and any(
            alergia in ingrediente or ingrediente in alergia
            for alergia in alergias
            for ingrediente in ingredientes
        ):
            continue
        if categorias and not any(
            categoria in tag or tag in categoria
            for categoria in categorias
            for tag in tags
        ):
            continue
        candidatos.append(prato)

    # Intercala categorias para evitar uma grade composta por receitas iguais.
    grupos = {}
    for prato in candidatos:
        chave = next(iter(prato.get("tags", [])), "sem categoria").casefold()
        grupos.setdefault(chave, []).append(prato)
    resultado = []
    while grupos and len(resultado) < limite:
        for chave in list(grupos):
            prato = grupos[chave].pop(0)
            resultado.append(prato)
            if not grupos[chave]:
                del grupos[chave]
            if len(resultado) >= limite:
                break

    return resultado

# Série auxiliar para busca por texto (montada 1x, no import)
_NOMES_LOWER = df["name"].astype(str).str.lower()
_IDS_DF = df["id"]


def buscar_pratos(query="", pagina=1, por_pagina=20, ingredientes=None):
    query = (query or "").strip().lower()
    ingredientes = [
        str(ingrediente).strip().casefold()
        for ingrediente in (ingredientes or [])
        if str(ingrediente).strip()
    ]
    por_pagina = max(1, min(por_pagina, 50))  # trava um teto, evita abuso
    pagina = max(1, pagina)

    ids_correspondentes = _IDS_DF.dropna().astype(int).tolist()

    if query:
        ids_query = set(
            _IDS_DF[
                _NOMES_LOWER.str.contains(query, na=False, regex=False)
            ].dropna().astype(int)
        )
        ids_correspondentes = [
            id_prato for id_prato in ids_correspondentes
            if id_prato in ids_query
        ]

    if ingredientes:
        ids_correspondentes = [
            id_prato
            for id_prato in ids_correspondentes
            if all(
                any(
                    ingrediente_filtro in str(ingrediente_prato).casefold()
                    for ingrediente_prato in _PRATOS_POR_ID[id_prato].get(
                        "ingredientes", []
                    )
                )
                for ingrediente_filtro in ingredientes
            )
        ]

    total = len(ids_correspondentes)
    inicio = (pagina - 1) * por_pagina
    fim = inicio + por_pagina
    ids_pagina = ids_correspondentes[inicio:fim]

    pratos = [_PRATOS_POR_ID[i] for i in ids_pagina if i in _PRATOS_POR_ID]

    return {
        "pratos": pratos,
        "total": total,
        "pagina": pagina,
        "por_pagina": por_pagina,
        "tem_mais": fim < total,
    }
    
alergias_df = pd.read_pickle(BASE_DIR / "dataset" / "ingr_map.pkl")

def obter_alergias():
    return alergias_df["replaced"].drop_duplicates().tolist()

PP_RECEITAS = pd.read_csv(
    BASE_DIR / "dataset" / "PP_recipes.csv",
    usecols=["id", "ingredient_ids"],
)
PP_RECEITAS["ingredient_ids"] = PP_RECEITAS["ingredient_ids"].apply(ast.literal_eval)


def obter_pares_receita_ingrediente(ids=None):
    """Retorna um set de (prato_id, ingrediente_id), sem duplicatas."""
    df = PP_RECEITAS
    if ids is not None:
        df = df[df["id"].isin(ids)]

    return {
        (int(prato_id), int(ing_id))
        for prato_id, lista in zip(df["id"], df["ingredient_ids"])
        for ing_id in lista
    }