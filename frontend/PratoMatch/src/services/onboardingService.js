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

export async function buscarPratosOnboarding({
  alergias = [],
  categorias = [],
  restricao = "nenhuma",
} = {}) {
  const params = new URLSearchParams();
  alergias.forEach((item) => params.append("alergias", item));
  categorias.forEach((item) => params.append("categorias", item));
  if (restricao && restricao !== "nenhuma") {
    params.set("restricao", restricao);
  }

  const response = await fetch(
    `${API_URL}/onboarding/pratos/?${params.toString()}`,
  );
  if (!response.ok) {
    throw new Error("Erro ao buscar pratos do onboarding.");
  }

  const data = await response.json();
  return Array.isArray(data.pratos) ? data.pratos : [];
}
