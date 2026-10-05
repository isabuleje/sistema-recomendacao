import { apiFetch } from "./api.js";

export async function buscarPerfil() {
  return await apiFetch("/perfil/")
}

