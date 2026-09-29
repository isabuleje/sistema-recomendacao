import { useEffect, useRef, useState } from "react";
import { pesquisarPratos } from "../services/Pratos.js";

const ATRASO_DEBOUNCE = 300;
export const POR_PAGINA_BUSCA = 24; //pra ficar igual a do home

export function useBuscaPratos(termo, pagina = 1) {
  const [resultados, setResultados] = useState([]);
  const [total, setTotal] = useState(0);
  const [buscando, setBuscando] = useState(false);
  const [erroBusca, setErroBusca] = useState(null);

  const idRequisicaoAtual = useRef(0);

  useEffect(() => {
    const termoLimpo = termo.trim();

    if (!termoLimpo) {
      setResultados([]);
      setTotal(0);
      setBuscando(false);
      setErroBusca(null);
      return;
    }

    const idRequisicao = ++idRequisicaoAtual.current;
    setBuscando(true);
    setErroBusca(null);

    const timer = setTimeout(async () => {
      try {
        const dados = await pesquisarPratos(
          termoLimpo,
          pagina,
          POR_PAGINA_BUSCA,
        );

        if (idRequisicao === idRequisicaoAtual.current) {
          setResultados(dados.pratos);
          setTotal(dados.total);
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
  }, [termo, pagina]);

  const emBusca = termo.trim().length > 0;

  return { resultados, total, buscando, erroBusca, emBusca };
}
