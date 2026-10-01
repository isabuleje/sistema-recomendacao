import { apiFetch } from 'api.js';

export async function buscarIngredientes() {
  return await apiFetch("/ingredientes/");
}

