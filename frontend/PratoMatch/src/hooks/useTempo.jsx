import { useState, useEffect, useRef } from "react";
import { buscarTempoVisualizado, salvarTempoVisualizado } from "../services/tempoService.js";

//Salva tempo de visualização de um prato

export function useTempo(pratoId, tempoVisualizadoInicial = 0) {
  const usaColecao = pratoId == null;
  const [tempoVisualizado, setTempoVisualizado] = useState(() =>
    usaColecao ? 0 : Number(tempoVisualizadoInicial),
  );
  const [carregando, setCarregando] = useState(false);
  const [salvando, setSalvando] = useState(false);
  const [erro, setErro] = useState("");

  useEffect(() => {
    async function carregar() {
      try {
        setCarregando(true);

        const dados = await buscarTempoVisualizado();

        setTempoVisualizado(Number(dados.tempoVisualizado));
      } catch (error) {
        console.error("Erro ao carregar tempo de visualização:", error);
      } finally {
        setCarregando(false);
      }
    }

    carregar();
  }, [pratoId, usaColecao]);

  return {
    tempoVisualizado,
    tempoVisualizados: usaColecao ? tempoVisualizado : pratoId,
    salvarTempoVisualizado,
    erro,
    carregando,
    salvando,
  };
}
