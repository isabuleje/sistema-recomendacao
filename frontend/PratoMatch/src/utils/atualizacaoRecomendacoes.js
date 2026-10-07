const CHAVE_AVALIACOES_PENDENTES =
  "pratomatch:avaliacoes-desde-recomendacoes";
const LIMITE_AVALIACOES = 5;

function lerAvaliacoes() {
  try {
    const valor = sessionStorage.getItem(CHAVE_AVALIACOES_PENDENTES);
    const ids = valor ? JSON.parse(valor) : [];

    return Array.isArray(ids) ? ids : [];
  } catch (error) {
    console.error("Erro ao ler o contador de avaliações:", error);
    return [];
  }
}

export function registrarAvaliacao(pratoId) {
  const ids = lerAvaliacoes();
  const id = String(pratoId);

  if (!ids.includes(id)) {
    ids.push(id);
  }

  try {
    sessionStorage.setItem(CHAVE_AVALIACOES_PENDENTES, JSON.stringify(ids));
  } catch (error) {
    console.error("Erro ao salvar o contador de avaliações:", error);
  }

  window.dispatchEvent(new Event("avaliacao-salva"));
}

export function deveAtualizarRecomendacoes() {
  return lerAvaliacoes().length >= LIMITE_AVALIACOES;
}

export function limparAvaliacoesPendentes() {
  try {
    sessionStorage.removeItem(CHAVE_AVALIACOES_PENDENTES);
  } catch (error) {
    console.error("Erro ao limpar o contador de avaliações:", error);
  }
}
