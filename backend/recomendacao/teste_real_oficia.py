from pathlib import Path
import pandas as pd

from metricas import ground_truth_por_nota, mrr_at_k
from algoritmos import recomendar_para

BASE_DIR = Path(__file__).resolve().parents[1]
dataset = BASE_DIR / "dataset"

validacao = pd.read_csv(dataset / "interactions_validation.csv")

ground_truth = ground_truth_por_nota(
    validacao.to_dict("records"),
    nota_minima=4,
)

rankings = {}
usuarios_ignorados = []

for usuario_id in ground_truth:

    try:
        recomendacoes = recomendar_para(
            usuario_id,
            limite=5
        )

        if recomendacoes is not None and len(recomendacoes) > 0:
            rankings[usuario_id] = recomendacoes
        else:
            usuarios_ignorados.append(usuario_id)

    except KeyError:
        usuarios_ignorados.append(usuario_id)


print("=" * 50)
print(f"Usuários na validação:      {len(ground_truth)}")
print(f"Usuários avaliados:         {len(rankings)}")
print(f"Usuários ignorados:         {len(usuarios_ignorados)}")
print("=" * 50)

resultado = mrr_at_k(
    rankings_por_usuario=rankings,
    itens_relevantes_por_usuario=ground_truth,
    k=5,
)

print(f"MRR@5: {resultado:.4f}")