import OnBoardingHeader from "../components/onboarding/OnBoardingHeader";
import SelecaoAlergias from "../components/onboarding/etapas/Etapa-Um";
import EscolhaPratos from "../components/onboarding/etapas/Etapa-Tres";

import { TOTAL_FASES} from "../constants/onboardingData.js";

import { useOnboarding } from "../hooks/useOnboarding";

import "../components/onboarding/css/OnBoardingLayout.css";
import "../components/onboarding/css/OnBoardingFase1.css";
import "../components/onboarding/css/OnBoardingFase3.css";

const OnBoarding = () => {
  const {
    fase,

    listaAlergias,

    alergia,
    setAlergia,

    alergias,
    adicionarAlergia,
    removerAlergia,

    pratosSelecionados,
    pratos,
    carregandoPratos,
    togglePrato,

    avancar,
    voltar,

    handleConcluir,

    salvando,
    erro,

    podeConcluir,
  } = useOnboarding();

  return (
    <section id="onboarding">
      <div className="onboarding-card">
        <OnBoardingHeader fase={fase} totalFases={TOTAL_FASES} />

        {erro && <div className="onboarding-erro">{erro}</div>}

        {fase === 1 && (
          <SelecaoAlergias
            alergia={alergia}
            setAlergia={setAlergia}
            alergias={alergias}
            adicionarAlergia={adicionarAlergia}
            removerAlergia={removerAlergia}
            onAvancar={avancar}
            opcoesAlergias={listaAlergias}
          />
        )}

        {fase === 2 && (
          <EscolhaPratos
            selecionados={pratosSelecionados}
            pratos={pratos}
            carregando={carregandoPratos}
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
