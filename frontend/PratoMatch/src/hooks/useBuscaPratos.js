import { useEffect, useRef, useState } from "react";
import { pesquisarPratos } from "../services/pratosService.js";
import { ATRASO_DEBOUNCE, POR_PAGINA_BUSCA } from "../constants/busca.js";

/* Hook utilizado para pesquisar pratos 
  Basicamente ele recebe o termo pesquisado
  Aplica o debounce (dar um tempo para que mande a informação para o backend)
  Evita que uma resposta antiga sobrescreva uma pesquisa mais recente
*/

export function useBuscaPratos() {
  // Pratos encontrados pela pesquisa.
  const [resultados, setResultados] = useState([]);
  const [total, setTotal] = useState(0);
  const [pagina, setPagina] = useState(1);
  const [termo, setTermo] = useState("");
  const [buscando, setBuscando] = useState(false); //se ta tendo busca, sim ou nao
  const [erroBusca, setErroBusca] = useState(null);

  //guarda o id da pesquisa mais recente
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

    // debounce, esperando o usuário terminar de digitar antes de mandar a requisição
    const timer = setTimeout(async () => {
      try {
        // conectando com o service
        const dados = await pesquisarPratos(
          termoLimpo,
          pagina,
          POR_PAGINA_BUSCA,
        );

        //resposta apenas a requisição de busca mais recente
        if (idRequisicao === idRequisicaoAtual.current) {
          setResultados(Array.isArray(dados.pratos) ? dados.pratos : []);

          setTotal(Number(dados.total) || 0);
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

    //timer pra uma pesquisa nao sobrepor a outra
    return () => {
      clearTimeout(timer);
    };
  }, [termo, pagina]);

  //se tem termo ent busca :D
  const emBusca = (termo ?? "").trim().length > 0;

  return {
    resultados,
    total,
    buscando,
    erroBusca,
    emBusca,
  };
}
