import { useEffect, useState } from "react";
import {
  MIN_PRATOS,
  TOTAL_FASES,
} from "../components/OnBoarding/onboardingData";
import {
  buscarCategorias,
  buscarIngredientes,
} from "../services/Ingredientes_Categorias.js";

import { salvarOnboarding } from "../services/OnBoarding.js";

export function useOnboarding() {
  const [fase, setFase] = useState(1);

  const [categorias, setCategorias] = useState([]);
  const [ingredientes, setIngredientes] = useState([]);

  const [restricao, setRestricao] = useState("nenhuma");

  const [alergia, setAlergia] = useState("");
  const [alergias, setAlergias] = useState([]);

  const [culinariasSelecionadas, setCulinariasSelecionadas] = useState([]);
  const [pratosSelecionados, setPratosSelecionados] = useState([]);

  const [salvando, setSalvando] = useState(false);
  const [erro, setErro] = useState(null);

  useEffect(() => {
    let ativo = true;

    async function carregarDados() {
      try {
        const [categoriasEncontradas, ingredientesEncontrados] =
          await Promise.all([buscarCategorias(), buscarIngredientes()]);

        if (!ativo) return;

        setCategorias(
          Array.isArray(categoriasEncontradas) ? categoriasEncontradas : [],
        );

        setIngredientes(
          Array.isArray(ingredientesEncontrados) ? ingredientesEncontrados : [],
        );
      } catch (error) {
        console.error("Erro ao carregar dados do onboarding:", error);

        if (ativo) {
          setErro("Não foi possível carregar os dados.");
        }
      }
    }

    carregarDados();

    return () => {
      ativo = false;
    };
  }, []);

  const adicionarAlergia = (ingrediente) => {
    setAlergias((anteriores) =>
      anteriores.includes(ingrediente)
        ? anteriores
        : [...anteriores, ingrediente],
    );

    setAlergia("");
  };

  const removerAlergia = (ingrediente) => {
    setAlergias((anteriores) =>
      anteriores.filter((item) => item !== ingrediente),
    );
  };

  const toggleCulinaria = (item) => {
    setCulinariasSelecionadas((atual) =>
      atual.includes(item)
        ? atual.filter((itemAtual) => itemAtual !== item)
        : [...atual, item],
    );
  };

  const togglePrato = (id) => {
    setPratosSelecionados((atual) =>
      atual.includes(id)
        ? atual.filter((prato) => prato !== id)
        : [...atual, id],
    );
  };

  const avancar = () => {
    setFase((atual) => Math.min(atual + 1, TOTAL_FASES));
  };

  const voltar = () => {
    setFase((atual) => Math.max(atual - 1, 1));
  };

  const obterDados = () => {
    return {
      restricao,
      alergias,
      culinarias: culinariasSelecionadas,
      pratos: pratosSelecionados,
    };
  };

  //Aqui é a parte mais importante pro backend

  const concluir = async () => {
    setSalvando(true);
    setErro(null);

    try {
      await salvarOnboarding({
        preferencias: restricao ? [restricao] : [],
        alergias: alergias, // lista de nomes
        categorias: culinariasSelecionadas, // lista de nomes das culinárias
        pratos_curtidos: pratosSelecionados, // lista de ids dos pratos
      });

      return true; 
    } catch (e) {
      setErro(e.message);
      return false;
    } finally {
      setSalvando(false);
    }
  };

  return {
    fase,
    categorias,
    ingredientes,
    restricao,
    setRestricao,
    alergia,
    setAlergia,
    alergias,
    adicionarAlergia,
    removerAlergia,
    culinariasSelecionadas,
    toggleCulinaria,
    pratosSelecionados,
    togglePrato,
    avancar,
    voltar,
    concluir,
    salvando,
    erro,

    podeConcluir: pratosSelecionados.length >= MIN_PRATOS,
  };
}
