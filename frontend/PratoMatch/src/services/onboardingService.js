import { apiFetch, prepararCsrf } from "./api.js";

/*
Os serviços do onboarding possue:
  - salvarOnboarding(dados)
  - listarAlergias()
  - buscarPratosOnboarding()
*/

/* Função POST que salva os dados escolhidos durante o onboarding*/
export async function salvarOnboarding(dados) {
  const csrfToken = await prepararCsrf();

  return apiFetch("/onboarding/", {
    method: "POST",

    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },

    body: JSON.stringify(dados),
  });
}

/* Função GET que pega todas as alergias*/
export async function listarAlergias() {
  const data = await apiFetch("/alergias/");

  return data;
}

/**
Busca os pratos que serão apresentados
durante o onboarding.

O filtro de alergias é opcional.

Tipo: 
buscarPratosOnboarding({
      alergias: [1, 3],
  });
 */
export async function buscarPratosOnboarding({
  alergias = [],
} = {}) {
  const params = new URLSearchParams();

  // Adiciona cada alergia separadamente
  alergias.forEach((item) => {
    params.append("alergias", item);
  });

  // Os parâmetros se transformam em uma URL
  const queryString = params.toString();

  const endpoint = queryString
    ? `/onboarding/pratos/?${queryString}`
    : "/onboarding/pratos/";

  const data = await apiFetch(endpoint);


  return Array.isArray(data.pratos) ? data.pratos : [];
}
