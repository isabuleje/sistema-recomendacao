import { useEffect, useRef, useState } from "react";
import { pesquisarPratos } from "../services/pratosService.js";
import { ATRASO_DEBOUNCE, POR_PAGINA_BUSCA } from "../constants/busca.js";

/* Hook utilizado para pesquisar pratos 
  Basicamente ele recebe o termo pesquisado
  Aplica o debounce (dar um tempo para que mande a informação para o backend)
  Evita que uma resposta antiga sobrescreva uma pesquisa mais recente
*/

export function useBuscaPratos() {
  const memoInicial = (() => {
    try {
      return JSON.parse(sessionStorage.getItem("busca-pratos")) || {};
    } catch {
      return {};
    }
  })();

  // Pratos encontrados pela pesquisa.
  const [resultados, setResultados] = useState([]);
  const [total, setTotal] = useState(0);
  const [pagina, setPagina] = useState(Number(memoInicial.pagina) || 1);
  const [termo, setTermo] = useState(memoInicial.termo || "");
  const [ingredientes, setIngredientes] = useState(
    Array.isArray(memoInicial.ingredientes) ? memoInicial.ingredientes : [],
  );
  const [buscando, setBuscando] = useState(false); //se ta tendo busca, sim ou nao
  const [erroBusca, setErroBusca] = useState(null);

  //guarda o id da pesquisa mais recente
  const idRequisicaoAtual = useRef(0);

  useEffect(() => {
    const termoLimpo = termo.trim();
    const idRequisicao = ++idRequisicaoAtual.current;

    sessionStorage.setItem(
      "busca-pratos",
      JSON.stringify({ termo, ingredientes, pagina }),
    );

    if (!termoLimpo && ingredientes.length === 0) {
      return;
    }

    const controller = new AbortController();

    // debounce, esperando o usuário terminar de digitar antes de mandar a requisição
    const timer = setTimeout(async () => {
      try {
        // conectando com o service
        const dados = await pesquisarPratos(
          termoLimpo,
          pagina,
          POR_PAGINA_BUSCA,
          controller.signal,
          ingredientes,
        );

        //resposta apenas a requisição de busca mais recente
        if (idRequisicao === idRequisicaoAtual.current) {
          setResultados(Array.isArray(dados.pratos) ? dados.pratos : []);

          setTotal(Number(dados.total) || 0);
        }
      } catch (error) {
        if (
          idRequisicao === idRequisicaoAtual.current &&
          error.name !== "AbortError"
        ) {
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
      controller.abort();
    };
  }, [termo, pagina, ingredientes]);

  //se tem termo ent busca :D
  const emBusca =
    (termo ?? "").trim().length > 0 || ingredientes.length > 0;
  const totalPaginas = Math.max(1, Math.ceil(total / POR_PAGINA_BUSCA));

  const alterarBusca = (event) => {
    const novoTermo = event.target.value;

    setTermo(novoTermo);
    setPagina(1);
    setResultados([]);
    setTotal(0);
    setErroBusca(null);
    setBuscando(novoTermo.trim().length > 0);
  };

  const limparBusca = () => {
    setTermo("");
    setIngredientes([]);
    setPagina(1);
    setResultados([]);
    setTotal(0);
    setBuscando(false);
    setErroBusca(null);
  };

  const adicionarIngrediente = (ingrediente) => {
    const ingredienteLimpo = ingrediente.trim();
    if (!ingredienteLimpo) return;

    setIngredientes((atuais) =>
      atuais.some(
        (item) =>
          item.toLocaleLowerCase() === ingredienteLimpo.toLocaleLowerCase(),
      )
        ? atuais
        : [...atuais, ingredienteLimpo],
    );
    setPagina(1);
    setResultados([]);
    setTotal(0);
  };

  const removerIngrediente = (ingrediente) => {
    setIngredientes((atuais) =>
      atuais.filter((item) => item !== ingrediente),
    );
    setPagina(1);
    setResultados([]);
    setTotal(0);
  };

  const mudarPagina = (novaPagina) => {
    setPagina(Math.min(Math.max(1, novaPagina), totalPaginas));
    setBuscando(true);
    setErroBusca(null);
  };

  return {
    termo,
    ingredientes,
    alterarBusca,
    limparBusca,
    adicionarIngrediente,
    removerIngrediente,
    pagina,
    mudarPagina,
    resultados,
    total,
    buscando,
    erro: erroBusca,
    erroBusca,
    emBusca,
    totalPaginas,
  };
}
