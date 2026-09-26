const API_URL = "http://127.0.0.1:8000/api";

export async function salvarOnboarding(dados) {
  const resposta = await fetch(`${API_URL}/onboarding/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(dados),
  });

  const resultado = await resposta.json();

  if (!resposta.ok) {
    throw new Error(
      resultado.erro || "Erro ao salvar o onboarding."
    );
  }

  return resultado;
}