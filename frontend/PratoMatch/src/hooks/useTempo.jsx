import { useState, useEffect } from "react";
import { buscarTempoVisualizado, salvarTempoVisualizado } from "../services/tempoService.js";

export function useTempo(pratoId, tempoVisualizadoInicial = 0) {
  const [tempoVisualizado, setTempoVisualizado] = useState(
    () => Number(tempoVisualizadoInicial) || 0,
  );
  const [carregando, setCarregando] = useState(false);
  const [erro, setErro] = useState("");

  useEffect(() => {
    if (pratoId == null) return undefined;

    let ativo = true;
    let podeSalvar = false;
    let acumulado = Number(tempoVisualizadoInicial) || 0;
    let marco = null;
    let intervalo = null;

    const publicar = () => {
      const atual =
        marco == null || document.hidden
          ? acumulado
          : acumulado + Math.floor((Date.now() - marco) / 1000);
      if (ativo) setTempoVisualizado(atual);
      return atual;
    };

    const persistir = (segundos) => {
      if (!podeSalvar) return;
      salvarTempoVisualizado(pratoId, segundos).catch((error) => {
        console.error("Erro ao salvar tempo de visualização:", error);
      });
    };

    async function iniciar() {
      try {
        setCarregando(true);
        setErro("");
        const dados = await buscarTempoVisualizado(pratoId);
        if (!ativo) return;
        acumulado = Number(dados?.tempo_visualizado) || 0;
        podeSalvar = true;
      } catch (error) {
        console.error("Erro ao carregar tempo de visualização:", error);
        if (ativo) {
          setErro(error.message || "Erro ao carregar o tempo de visualização.");
        }
      } finally {
        if (ativo) setCarregando(false);
      }

      if (!ativo) return;
      marco = document.hidden ? null : Date.now();
      publicar();

      intervalo = setInterval(() => {
        const anterior = acumulado;
        const atual = publicar();
        if (atual !== anterior && atual > 0 && atual % 10 === 0) {
          persistir(atual);
        }
      }, 1000);
    }

    const aoMudarVisibilidade = () => {
      if (!podeSalvar) return;
      if (document.hidden) {
        acumulado = publicar();
        marco = null;
        persistir(acumulado);
        return;
      }
      marco = Date.now();
    };

    document.addEventListener("visibilitychange", aoMudarVisibilidade);
    iniciar();

    return () => {
      ativo = false;
      if (intervalo) clearInterval(intervalo);
      document.removeEventListener("visibilitychange", aoMudarVisibilidade);
      if (!podeSalvar) return;
      const atual =
        marco == null
          ? acumulado
          : acumulado + Math.floor((Date.now() - marco) / 1000);
      persistir(atual);
    };
  }, [pratoId, tempoVisualizadoInicial]);

  return {
    tempoVisualizado,
    erro,
    carregando,
  };
}
