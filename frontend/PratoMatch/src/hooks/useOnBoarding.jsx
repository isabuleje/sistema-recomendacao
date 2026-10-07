import { useEffect, useState } from "react";
import { MIN_PRATOS, TOTAL_FASES } from "../constants/onboardingData.js";
import {
  salvarOnboarding,
  listarAlergias,
  buscarPratosOnboarding,
} from "../services/onboardingService.js";
import { useNavigate } from "react-router-dom";

export function useOnboarding() {
  const [fase, setFase] = useState(1); // são 2 fases

  const [listaAlergias, setListaAlergias] = useState([]);

  const [alergia, setAlergia] = useState(""); //texto q esta sendo digitado no input das alergias
  const [alergias, setAlergias] = useState([]); //alergias selecionadas pelo usuario

  const [pratosSelecionados, setPratosSelecionados] = useState([]);
  const [pratos, setPratos] = useState([]);
  const [carregandoPratos, setCarregandoPratos] = useState(false);

  const [salvando, setSalvando] = useState(false);
  const [erro, setErro] = useState(null);

  const navigate = useNavigate();

  // Carrega os dados necessários para o onboarding.
  useEffect(() => {
    let ativo = true; // flag para controlar se o componente ainda está montado

    async function carregarDados() {
      const alergiasRes = await Promise.allSettled([listarAlergias()]);
      const [resultadoAlergias] = alergiasRes;

      if (!ativo) return; //senao foi montado, nao faz nada

      if (resultadoAlergias.status === "fulfilled") {
        setListaAlergias(
          Array.isArray(resultadoAlergias.value)
            ? resultadoAlergias.value
            : [],
        );
      } else {
        console.error(
          "Erro ao buscar alergias:",
          resultadoAlergias.reason,
        );
        setErro("Não foi possível carregar a lista de alergias.");
      }
    }

    carregarDados();
    return () => {
      ativo = false;
    };
  }, []);

  // Carrega os pratos da fase 2 quando as alergias mudam.
  useEffect(() => {
    if (fase !== 2) return;

    let ativo = true;

    async function carregarPratos() {
      setCarregandoPratos(true);
      setErro(null);
      try {
        const resultado = await buscarPratosOnboarding({
          alergias,
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
  }, [fase, alergias]);

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

  // Alterna a seleção de um prato (fase 2)
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
    listaAlergias,
    pratos,

    //escolhas do usuário
    alergia,
    setAlergia,
    alergias,
    adicionarAlergia,
    removerAlergia,
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
