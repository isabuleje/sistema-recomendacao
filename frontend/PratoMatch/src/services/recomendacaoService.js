import { apiFetch } from "./api";

/*
Os serviços de recomendação possue a função:
  - buscarRecomendados()
*/

export async function buscarRecomendados() {
  const data = await apiFetch("/recomendados/");

  return data.pratos;
}
