import { apiFetch } from 'api.js';


/* Função GET para pegar todas as categorias*/
export async function buscarCategorias() {
  return await apiFetch("/categorias/")
}
