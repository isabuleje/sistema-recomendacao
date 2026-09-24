from pathlib import Path
import pandas as pd
import ast

# Ler CSV e mostrar as receitas encontradas
BASE_DIR = Path(__file__).resolve().parent.parent

RECEITAS = pd.read_csv(BASE_DIR / "dataset" / "RAW_recipes.csv")
INTERACOES = pd.read_csv(
    BASE_DIR / "dataset" / "RAW_interactions.csv"
)

print(f"Receitas encontradas: {len(RECEITAS)}")


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
            categoria
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
            ingrediente.strip()
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

def obter_pratos():

    pratos = []

    for _, prato in df.iterrows():

        pratos.append({

            "id": (
                int(prato["id"])
                if pd.notna(prato["id"])
                else None
            ),

            "nome": (
                str(prato["name"]).strip()
                if pd.notna(prato["name"])
                else "Prato sem nome"
            ),

            "descricao": (
                str(prato["description"]).strip()
                if pd.notna(prato["description"])
                else ""
            ),

            "tempo_preparo": (
                int(prato["minutes"])
                if pd.notna(prato["minutes"])
                else 0
            ),

            "estrelas": (
                round(float(prato["estrelas"]), 1)
                if pd.notna(prato["estrelas"])
                else 0
            ),

            "avaliacoes": (
                int(prato["avaliacoes"])
                if pd.notna(prato["avaliacoes"])
                else 0
            ),

            "tags": (
                prato["categorias"]
                if isinstance(prato["categorias"], list)
                else []
            ),

            "ingredientes": (
                prato["ingredients"]
                if isinstance(prato["ingredients"], list)
                else []
            ),

        })

    return pratos

