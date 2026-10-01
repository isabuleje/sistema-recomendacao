import { useEffect, useState } from "react";
import {
  MIN_PRATOS,
  TOTAL_FASES,
} from "../components/OnBoarding/onboardingData";
import { buscarCategorias } from "../services/Ingredientes_Categorias.js";

import {
  salvarOnboarding,
  listar_alergias,
  buscarPratosOnboarding,
} from "../services/onboardingService.js";

export function useOnboarding() {
  const [fase, setFase] = useState(1);

  const [categorias, setCategorias] = useState([]);
  const [listaAlergias, setListaAlergias] = useState([]);

  const [restricao, setRestricao] = useState("nenhuma");

  const [alergia, setAlergia] = useState("");
  const [alergias, setAlergias] = useState([]);

  const [culinariasSelecionadas, setCulinariasSelecionadas] = useState([]);
  const [pratosSelecionados, setPratosSelecionados] = useState([]);
  const [pratos, setPratos] = useState([]);
  const [carregandoPratos, setCarregandoPratos] = useState(false);

  const [salvando, setSalvando] = useState(false);
  const [erro, setErro] = useState(null);

  useEffect(() => {
    let ativo = true;

    async function carregarDados() {
      const [categoriasRes, alergiasRes] = await Promise.allSettled([
        buscarCategorias(),
        listar_alergias(),
      ]);

      if (!ativo) return;

      if (categoriasRes.status === "fulfilled") {
        setCategorias(
          Array.isArray(categoriasRes.value) ? categoriasRes.value : [],
        );
      }

      if (alergiasRes.status === "fulfilled") {
        setListaAlergias(
          Array.isArray(alergiasRes.value) ? alergiasRes.value : [],
        );
      } else {
        console.error("Erro ao buscar alergias:", alergiasRes.reason);
        setErro("Não foi possível carregar a lista de alergias.");
      }
    }

    carregarDados();
    return () => {
      ativo = false;
    };
  }, []);

  useEffect(() => {
    if (fase !== 3) return;

    let ativo = true;

    async function carregarPratos() {
      setCarregandoPratos(true);
      try {
        const resultado = await buscarPratosOnboarding({
          alergias,
          categorias: culinariasSelecionadas,
          restricao,
        });
        if (ativo) setPratos(resultado);
      } catch (erroBusca) {
        if (ativo) {
          console.error("Erro ao buscar pratos do onboarding:", erroBusca);
          setErro("Não foi possível carregar os pratos.");
        }
      } finally {
        if (ativo) setCarregandoPratos(false);
      }
    }

    carregarPratos();

    return () => {
      ativo = false;
    };
  }, [fase, alergias, culinariasSelecionadas, restricao]);

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

  const concluir = async () => {
    setSalvando(true);
    setErro(null);

    try {
      await salvarOnboarding({
        preferencias: restricao && restricao !== "nenhuma" ? [restricao] : [],
        alergias,
        categorias: culinariasSelecionadas,
        pratos_curtidos: pratosSelecionados,
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
    listaAlergias,
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
    pratos,
    carregandoPratos,
    togglePrato,
    avancar,
    voltar,
    concluir,
    salvando,
    erro,

    podeConcluir: pratosSelecionados.length >= MIN_PRATOS,
  };
}
