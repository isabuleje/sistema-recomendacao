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
