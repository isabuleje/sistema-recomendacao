import { useEffect, useState } from "react";
import { MIN_PRATOS, TOTAL_FASES } from "../constants/onboardingData.js";
import {
  salvarOnboarding,
  listarAlergias,
  buscarCategorias,
  buscarPratosOnboarding,
} from "../services/onboardingService.js";
import { useNavigate } from "react-router-dom";

export function useOnboarding() {
  const [fase, setFase] = useState(1); //sao 3 fases

  const [categorias, setCategorias] = useState([]);
  const [listaAlergias, setListaAlergias] = useState([]);

  const [alergia, setAlergia] = useState(""); //texto q esta sendo digitado no input das alergias
  const [alergias, setAlergias] = useState([]); //alergias selecionadas pelo usuario

  const [culinariasSelecionadas, setCulinariasSelecionadas] = useState([]);
  const [pratosSelecionados, setPratosSelecionados] = useState([]);
  const [pratos, setPratos] = useState([]);
  const [carregandoPratos, setCarregandoPratos] = useState(false);

  const [salvando, setSalvando] = useState(false);
  const [erro, setErro] = useState(null);

  const navigate = useNavigate();

  // carrega os dados necessários (categorias e alergias)
  useEffect(() => {
    let ativo = true; // flag para controlar se o componente ainda está montado

    async function carregarDados() {
      const [categoriasRes, alergiasRes] = await Promise.allSettled([
        buscarCategorias(),
        listarAlergias(),
      ]);

      if (!ativo) return; //senao foi montado, nao faz nada

      if (categoriasRes.status === "fulfilled") {
        setCategorias(
          Array.isArray(categoriasRes.value) ? categoriasRes.value : [],
        );
      } else {
        console.log("Erro ao buscar categorias:", categoriasRes.reason);
        setErro("Não foi possível carregar a lista de categorias.");
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

  // Carrega os pratos da fase 3 quando alergias ou categorias mudam.
  useEffect(() => {
    if (fase !== 3) return;

    let ativo = true;

    async function carregarPratos() {
      setCarregandoPratos(true);
      setErro(null);
      try {
        const resultado = await buscarPratosOnboarding({
          alergias,
          categorias: culinariasSelecionadas,
        });
        if (ativo) {
          setPratos(resultado);
        }
      } catch (erroBusca) {
        if (ativo) {
          console.error("Erro ao buscar pratos do onboarding:", erroBusca);
          setErro("Não foi possível carregar os pratos.");
        }
      } finally {
        if (ativo) {
          setCarregandoPratos(false);
        }
      }
    }

    carregarPratos();

    return () => {
      ativo = false;
    };
  }, [fase, alergias, culinariasSelecionadas]);

  // Adiciona alergias, e evita que uma mesma alergia seja selecionada duas vezes
  const adicionarAlergia = (ingrediente) => {
    setAlergias((anteriores) =>
      anteriores.includes(ingrediente)
        ? anteriores
        : [...anteriores, ingrediente],
    );

    setAlergia(""); //limpa o input
  };

  // Remove uma alergia da lista
  const removerAlergia = (ingrediente) => {
    setAlergias((anteriores) =>
      anteriores.filter((item) => item !== ingrediente),
    );
  };

  // Alterna a seleção de uma culinária (categoria/ fase 2)
  const toggleCulinaria = (item) => {
    setCulinariasSelecionadas((atual) => {
      if (atual.includes(item)) {
        return atual.filter((culinaria) => culinaria !== item);
      } else {
        return [...atual, item];
      }
    });
  };

  // Alterna a seleção de um prato (fase 3)
  const togglePrato = (id) => {
    setPratosSelecionados((atual) =>{
      if (atual.includes(id)) {
        return atual.filter((pratoId) => pratoId !== id);
      } else {
        return [...atual, id];
      }
    })
  };


  // Funções para avançar e voltar entre as fases do onboarding, garantindo que não ultrapasse os limites
  const avancar = () => {
    setFase((atual) => Math.min(atual + 1, TOTAL_FASES));
  };

  const voltar = () => {
    setFase((atual) => Math.max(atual - 1, 1));
  };


  // Concluir envia todas as escolhas do usuário para o backend
  const concluir = async () => {
    setSalvando(true);
    setErro(null);

    try {
      await salvarOnboarding({
        alergias,
        categorias: culinariasSelecionadas,
        pratos_curtidos: pratosSelecionados,
      });

      return true;
    } catch (e) {
      console.log("Erro ao salvar onboarding:", e);
      setErro(e.message || "Erro ao salvar o onboarding. Tente novamente.");
      return false;
    } finally {
      setSalvando(false);
    }
  };

  const podeConcluir = pratosSelecionados.length >= MIN_PRATOS;

  const handleConcluir = async () => {
    const sucesso = await concluir();

    if (sucesso) {
      navigate("/home");
    }
  };

  return {
    //navegação entre fases
    fase,
    avancar,
    voltar,

    //dados do onboarding
    categorias,
    listaAlergias,
    pratos,

    //escolhas do usuário
    alergia,
    setAlergia,
    alergias,
    adicionarAlergia,
    removerAlergia,
    culinariasSelecionadas,
    toggleCulinaria,
    pratosSelecionados,
    togglePrato,
    

    //operacoes
    concluir,
    carregandoPratos,
    salvando,
    erro,
    handleConcluir,

    //condicao para habilitar o botão de concluir
    podeConcluir,
  };
}
