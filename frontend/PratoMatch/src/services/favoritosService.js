import { apiFetch, prepararCsrf } from "./api.js";

/*
Serviços para os favoritos:
    - buscarFavoritos()
    - salvarFavorito()
*/

/* Função GET para buscar todos os pratos que foram favoritados*/
export async function buscarFavoritos() {
  return apiFetch("/favoritos/");
}

/* 
Função POST para remover ou salvar um prato dos favoritos
    - pratoId (ID do prato)
    - favorito (bool se o prato está favoritado ou não)
*/
export async function salvarFavorito(prato_id, favorito) {
  const csrfToken = await prepararCsrf();

  return apiFetch("/favoritos/salvar", {
    method: "POST",

    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
    body: JSON.stringify({
        prato_id: prato_id,
        status: favorito ? "Favoritado" : "Avaliado"
    })
  });
}
