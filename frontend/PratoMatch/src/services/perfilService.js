import { API_URL } from "./api.js";

export async function buscarPerfil() {
  const response = await fetch(`${API_URL}/perfil/`, {
    credentials: "include",
  })

  if (!response.ok) {
    throw new Error("Erro ao buscar perfil");
  }

  return response.json(); // { preferencias: [...], alergias: [...], usuario_id, username }
                          //tudo q eu vou usar na t ela de perfil
}

