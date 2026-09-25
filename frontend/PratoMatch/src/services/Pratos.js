const API_URL = "http://127.0.0.1:8000/api";

export async function buscarPratos() {
  const response = await fetch(`${API_URL}/pratos_data/`);

  if (!response.ok) {
    throw new Error("Erro ao buscar pratos");
  }

  const data = await response.json();

  return data.pratos;
}
