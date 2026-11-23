import { apiFetch } from "./api.js";

/*
Serviços do prato:
  - buscarPratos()
  - buscarPrato(id)
  - pesquisarPratos(query, pagina, porPagina, signal)
*/

/* Função GET para buscar todos os pratos disponíveis no SQLite*/
export async function buscarPratos() {
  const data = await apiFetch("/pratos_data/");
  return data.pratos;
}

/* Função GET para pegar prato com ID específico */
export async function buscarPratoFavoritados(id) {
  return apiFetch(`/pratos/${id}/`);
}

/* 
Função GET para buscar pratos pelo NOME 
  - query (texto pesquisado)
  - pagina (página atual)
  - porPagina (quantidade de resultados)
  - signal (permite cancelar a requisição)
*/
export async function pesquisarPratos(
  query,
  pagina = 1,
  porPagina = 20,
  signal,
  ingredientes = [],
) {
  const params = new URLSearchParams({
    q: query,
    pagina: String(pagina),
    por_pagina: String(porPagina),
  });
  ingredientes.forEach((ingrediente) => {
    params.append("ingrediente", ingrediente);
  });

  return apiFetch(`/pesquisar/?${params}`,{
    signal,
  })
}

export async function buscarIngredientes() {
  const data = await apiFetch("/ingredientes/");
  return Array.isArray(data.ingredientes) ? data.ingredientes : [];
}
