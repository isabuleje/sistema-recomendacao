import { apiFetch, prepararCsrf } from "./api.js";

/*
Serviços para a avaliação possui:
  - salvarAvaliacao(pratoId, nota)
  - buscarAvaliados
*/

export async function buscarAvaliados() {
    return apiFetch("/avaliados/");
}

/* Função para salvar avaliação que recebe ID do prato e a nota do usuário*/
export async function salvarAvaliacao(pratoId, nota) {
  const csrfToken = await prepararCsrf();

  return apiFetch("/avaliacoes/", {
    method: "POST",

    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },

    body: JSON.stringify({
        prato_id: pratoId,
        nota
    })
  });
}
