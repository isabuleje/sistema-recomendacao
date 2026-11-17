import { apiFetch, prepararCsrf } from "./api.js";

/*
Os serviços do onboarding possue:
  - salvarOnboarding(dados)
  - listarAlergias()
  - buscarCategorias()
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

Os filtros são opcionais:
  - alergias
  - categorias
  - alergias e categorias

Tipo: 
buscarPratosOnboarding({
      alergias: [1, 3],
      categorias: ["italiana", "brasileira"]
  });

Tenho quase certeza que o backend não funciona dessa maneira, uma das coisas para MUDAR
 */
export async function buscarPratosOnboarding({
  alergias = [],
  categorias = [],
} = {}) {
  const params = new URLSearchParams();

  // Adiciona cada alergia separadamente
  alergias.forEach((item) => {
    params.append("alergias", item);
  });

  // Categorias também indo separads
  categorias.forEach((item) => {
    params.append("categorias", item);
  });

  // Os parâmetros se transformam em uma URL
  const queryString = params.toString();

  const endpoint = queryString
    ? `/onboarding/pratos/?${queryString}`
    : "/onboarding/pratos/";

  const data = await apiFetch(endpoint);


  return Array.isArray(data.pratos) ? data.pratos : [];
}

/* Função GET para pegar todas as categorias*/
export async function buscarCategorias() {
  const data = await apiFetch("/categorias/");
  return Array.isArray(data) ? data : (data?.categorias ?? []);
}
