import { API_URL, prepararCsrf } from "./api.js";

export async function salvarOnboarding(dados) {
  const csrfToken = await prepararCsrf();
  const resposta = await fetch(`${API_URL}/onboarding/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
    credentials: "include",
    body: JSON.stringify(dados),
  });

  const resultado = await resposta.json();

  if (!resposta.ok) {
    throw new Error(resultado.erro || "Erro ao salvar o onboarding.");
  }

  return resultado;
}

export async function listar_alergias() {
  const response = await fetch(`${API_URL}/alergias/`);

  if (!response.ok) {
    throw new Error(`Erro ao buscar alergias: ${response.status}`);
  }

  const alergias = await response.json();
  return alergias;
}
