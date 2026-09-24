import { useEffect, useState } from "react";
import OnBoardingHeader from "../components/OnBoarding/OnBoardingHeader";
import RestricaoAlimentar from "../components/OnBoarding/RestricaoAlimentar";
import EscolhaCulinaria from "../components/OnBoarding/EscolhaCulinaria";
import EscolhaPratos from "../components/OnBoarding/EscolhaPratos";
import {
  MIN_PRATOS,
  TOTAL_FASES,
} from "../components/OnBoarding/onboardingData";
import "../components/OnBoarding/OnBoardingLayout.css";
import "../components/OnBoarding/OnBoardingFase1.css";
import "../components/OnBoarding/OnBoardingFase2.css";
import "../components/OnBoarding/OnBoardingFase3.css";

import {buscarCategorias, buscarIngredientes} from "../services/Ingredientes_Categorias.js"

const OnBoarding = ({ onConcluir }) => {
  const [fase, setFase] = useState(1);
  const [categorias, setCategorias] = useState([]);
  const [ingredientes, setIngredientes] = useState([]);
  const [restricao, setRestricao] = useState("nenhuma");
  const [alergia, setAlergia] = useState("");
  const [alergias, setAlergias] = useState([]);
  const [culinariasSelecionadas, setCulinariasSelecionadas] = useState([]);
  const [pratosSelecionados, setPratosSelecionados] = useState([]);

  useEffect(() => {
    let ativo = true;

    Promise.all([buscarCategorias(), buscarIngredientes()])
      .then(([categoriasEncontradas, ingredientesEncontrados]) => {
        if (!ativo) return;

        setCategorias(Array.isArray(categoriasEncontradas) ? categoriasEncontradas : []);
        setIngredientes(Array.isArray(ingredientesEncontrados) ? ingredientesEncontrados : []);
      })
      .catch((error) => {
        console.error("Erro ao carregar dados do onboarding:", error);
      });

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

  const avancar = () => setFase((atual) => Math.min(atual + 1, TOTAL_FASES));
  const voltar = () => setFase((atual) => Math.max(atual - 1, 1));

  const handleConcluir = () => {
    const preferencias = {
      restricao,
      alergias,
      culinarias: culinariasSelecionadas,
      pratos: pratosSelecionados,
    };

    if (onConcluir) {
      onConcluir(preferencias);
    } else {
      console.log("Preferências salvas:", preferencias);
    }
  };

  return (
    <section id="onboarding">
      <div className="onboarding-card">
        <OnBoardingHeader fase={fase} totalFases={TOTAL_FASES} />

        {fase === 1 && (
          <RestricaoAlimentar
            restricao={restricao}
            setRestricao={setRestricao}
            alergia={alergia}
            setAlergia={setAlergia}
            alergias={alergias}
            adicionarAlergia={adicionarAlergia}
            removerAlergia={removerAlergia}
            onAvancar={avancar}
            ingredientes={ingredientes}
          />
        )}

        {fase === 2 && (
          <EscolhaCulinaria
            selecionadas={culinariasSelecionadas}
            onToggle={toggleCulinaria}
            onVoltar={voltar}
            onAvancar={avancar}
            podeAvancar={culinariasSelecionadas.length > 0}
            categorias={categorias}
          />
        )}

        {fase === 3 && (
          <EscolhaPratos
            selecionados={pratosSelecionados}
            onToggle={togglePrato}
            onVoltar={voltar}
            onConcluir={handleConcluir}
            podeConcluir={pratosSelecionados.length >= MIN_PRATOS}
          />
        )}
      </div>
    </section>
  );
};

export default OnBoarding;
