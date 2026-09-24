const API_URL = "http://127.0.0.1:8000/api";

export async function buscarCategorias() {
  const response = await fetch(`${API_URL}/categorias/`);

  if (!response.ok) {
    throw new Error("Erro ao buscar categorias");
  }

  const data = await response.json();

  return data.categorias;
}


export async function buscarIngredientes() {
  const response = await fetch(`${API_URL}/ingredientes/`);

  if (!response.ok) {
    throw new Error("Erro ao buscar ingredientes");
  }

  const data = await response.json();

  return data.ingredientes;
}