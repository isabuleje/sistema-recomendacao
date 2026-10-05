import { apiFetch } from "./api";

/*
Os serviços de recomendação possue a função:
  - buscarRecomendados()
*/

export async function buscarRecomendados() {
  const data = await apiFetch("/recomendados/");
  console.log("[recomendados] pratos recebidos no frontend:", data.pratos);

  return data.pratos;
}
