import { API_URL, prepararCsrf } from "./api.js";

export async function buscarPratos() {
  const response = await fetch(`${API_URL}/pratos_data/`, {
    credentials: "include",
  });

  if (!response.ok) {
    throw new Error("Erro ao buscar pratos");
  }

  const data = await response.json();

  return data.pratos;
}

export async function buscarPratoFavoritados() {
  const response = await fetch(`${API_URL}/favoritos/`, {
    credentials: "include",
  });

  if (!response.ok) {
    throw new Error("Erros ao buscar pratos favoritados");
  }

  return response.json();
}

export async function salvarFavoritos(pratoId, favorito) {
  const csrfToken = await prepararCsrf();
  const response = await fetch(`${API_URL}/favoritos/salvar/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
    credentials: "include",
    body: JSON.stringify({
      prato_id: pratoId,
      status: favorito ? "Favoritado" : "Avaliado",
    }),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.erro || "Erro ao salvar o favorito");
  }

  return data;
}

export async function buscarPratosAvaliados() {
  const response = await fetch(`${API_URL}/avaliados/`, {
    credentials: "include",
  });

  if (!response.ok) {
    throw new Error("Erro ao buscar pratos avaliados");
  }

  return response.json();
}

export async function salvarAvaliacao(pratoId, nota) {
  const csrfToken = await prepararCsrf();
  const response = await fetch(`${API_URL}/avaliacoes/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
    credentials: "include",
    body: JSON.stringify({ prato_id: pratoId, nota }),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.erro || "Erro ao salvar avaliação");
  }

  return data;
}

export async function pesquisarPratos(
  query,
  pagina = 1,
  porPagina = 20,
  signal,
) {
  const params = new URLSearchParams({
    q: query,
    pagina,
    por_pagina: porPagina,
  });
  const response = await fetch(`${API_URL}/pesquisar/?${params}`, {
    credentials: "include",
    signal,
  });

  if (!response.ok) {
    throw new Error("Erro ao pesquisar pratos");
  }

  return response.json(); // { pratos, total, pagina, por_pagina, tem_mais }
}
