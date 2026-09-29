import { useEffect, useRef, useState } from "react";
import { pesquisarPratos } from "../services/Pratos.js";

const ATRASO_DEBOUNCE = 300;

export function useBuscaPratos(termo) {
  const [resultados, setResultados] = useState([]);
  const [buscando, setBuscando] = useState(false);
  const [erroBusca, setErroBusca] = useState(null);

  // evita que uma resposta antiga e lenta sobrescreva uma busca mais nova
  const idRequisicaoAtual = useRef(0);

  useEffect(() => {
    const termoLimpo = termo.trim();

    if (!termoLimpo) {
      setResultados([]);
      setBuscando(false);
      setErroBusca(null);
      return;
    }

    const idRequisicao = ++idRequisicaoAtual.current;
    setBuscando(true);
    setErroBusca(null);

    const timer = setTimeout(async () => {
      try {
        const dados = await pesquisarPratos(termoLimpo, 1, 20);

        if (idRequisicao === idRequisicaoAtual.current) {
          setResultados(dados.pratos);
        }
      } catch (error) {
        if (idRequisicao === idRequisicaoAtual.current) {
          console.error("Erro ao pesquisar pratos:", error);
          setErroBusca("Não foi possível buscar os pratos.");
        }
      } finally {
        if (idRequisicao === idRequisicaoAtual.current) {
          setBuscando(false);
        }
      }
    }, ATRASO_DEBOUNCE);

    return () => clearTimeout(timer);
  }, [termo]);

  const emBusca = termo.trim().length > 0;

  return { resultados, buscando, erroBusca, emBusca };
}