/*
Váriaveis estáticas do onboarding
Aqui pode alterar:
  - Restrições alimentares
  - Total de etapas/fases no onboarding
  - Mínimo de escolha de pratos na fase 3
*/

export const RESTRICOES = [
  {
    value: "nenhuma",
    label: "Nenhuma",
    icone: "🍽️",
    descricao: "Não tenho restrições alimentares",
  },
  {
    value: "vegetariano",
    label: "Vegetariano",
    icone: "🌿",
    descricao: "Não como carne animal (ex: Frango, Boi, Porco).",
  },
  {
    value: "vegano",
    label: "Vegano",
    icone: "🥬",
    descricao: "Não como nenhum produto de origem animal",
  },
  {
    value: "gluten",
    label: "Sem glúten",
    icone: "🌾",
    descricao: "Evito alimentos com glúten",
  },
  {
    value: "lactose",
    label: "Sem lactose",
    icone: "🥛",
    descricao: "Evito alimentos com lactose",
  },
];

export const TOTAL_FASES = 3;
export const MIN_PRATOS = 3;
