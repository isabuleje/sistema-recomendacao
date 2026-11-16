import { apiFetch, prepararCsrf } from "./api.js";

/*
Serviços para o tempo de visualização:
    - salvarTempoVisualizado()
    - buscarTempoVisualizado()
*/

/* 
Função POST para salvar o tempo de visualização de um prato
    - pratoId (ID do prato)
    - tempoVisualizado (tempo de visualização em segundos)
*/
export async function salvarTempoVisualizado(prato_id, tempoVisualizado) {
  const csrfToken = await prepararCsrf();

  return apiFetch("/tempo/visualizado/salvar/", {
    method: "POST",

    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
    body: JSON.stringify({
      prato_id,
      tempo_visualizado: tempoVisualizado,
    }),
  });
}

/* 
Função GET para buscar o tempo de visualização de um prato
    - pratoId (ID do prato)
*/
export async function buscarTempoVisualizado(pratoId) {
  return apiFetch(`/tempo/visualizado/buscar/?prato_id=${pratoId}`);
}