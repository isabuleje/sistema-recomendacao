from pathlib import Path
import pandas as pd
import ast

# Ler CSV e mostrar as receitas encontradas
BASE_DIR = Path(__file__).resolve().parent.parent
df = pd.read_csv(BASE_DIR / "dataset" / "RAW_recipes.csv")
print(f"Receitas encontradas: {len(df)}")


#Tags e ingredientes estão como string, então tem que converter para lista
df["tags"] = df["tags"].apply(
    lambda x: ast.literal_eval(x) if isinstance(x, str) else []
)

df["ingredients"] = df["ingredients"].apply(
    lambda x: ast.literal_eval(x) if isinstance(x, str) else []
)

import pandas as pd
import ast


# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

ARQUIVO_CSV = "RAW_recipes.csv"


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

    # tags sus
    "Throw the ultimate fiesta with this sopaipillas recipe from Food.com.",
    "less_thansql:name_topics_of_recipegreater_than",
}


tags_ignorar = {
    tag.lower().strip()
    for tag in TAGS_IGNORAR
}

def limpar_tags(tags):

    resultado = []

    for tag in tags:

        if not isinstance(tag, str):
            continue

        tag = tag.strip()

        if not tag:
            continue

        if tag.lower() in tags_ignorar:
            continue

        resultado.append(tag)

    return resultado


df["categorias"] = df["tags"].apply(limpar_tags)


#Categorias únicas para mostrar no frontend, lá no OnBoarding
categorias_unicas = sorted(
    {
        categoria
        for lista in df["categorias"]
        for categoria in lista
    },
    key=str.lower
)

print(f"Categorias encontradas: {len(categorias_unicas)}")
print(categorias_unicas)


#Ingredientes únicos para dps verificar alergias e restrições 
ingredientes_unicos = sorted(
    {
        ingrediente.strip()
        for lista in df["ingredients"]
        for ingrediente in lista
        if isinstance(ingrediente, str)
        and ingrediente.strip()
    },
    key=str.lower
)

print(f"Ingredientes encontrados: {len(ingredientes_unicos)}")