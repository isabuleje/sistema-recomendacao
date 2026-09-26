import { useNavigate } from "react-router-dom";

import OnBoardingHeader from "../components/OnBoarding/OnBoardingHeader";
import RestricaoAlimentar from "../components/OnBoarding/RestricaoAlimentar";
import EscolhaCulinaria from "../components/OnBoarding/EscolhaCulinaria";
import EscolhaPratos from "../components/OnBoarding/EscolhaPratos";

import { TOTAL_FASES } from "../components/OnBoarding/onboardingData";

import { useOnboarding } from "../hooks/useOnBoarding";

import "../components/OnBoarding/OnBoardingLayout.css";
import "../components/OnBoarding/OnBoardingFase1.css";
import "../components/OnBoarding/OnBoardingFase2.css";
import "../components/OnBoarding/OnBoardingFase3.css";

const OnBoarding = () => {
  const navigate = useNavigate();

  const {
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

    podeConcluir,
  } = useOnboarding();

  const handleConcluir = async () => {
    const sucesso = await concluir();

    if (sucesso) {
      navigate("/");
    }
  };

  return (
    <section id="onboarding">
      <div className="onboarding-card">
        <OnBoardingHeader fase={fase} totalFases={TOTAL_FASES} />

        {erro && <div className="onboarding-erro">{erro}</div>}

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
            podeConcluir={podeConcluir}
            salvando={salvando}
          />
        )}
      </div>
    </section>
  );
};

export default OnBoarding;
