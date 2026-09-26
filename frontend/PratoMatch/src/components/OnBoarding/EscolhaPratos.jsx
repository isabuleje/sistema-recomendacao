import CardPratoCirculo from "./CardPratoCirculo";
import { MIN_PRATOS, PRATOS } from "./onboardingData";
import { ArrowRight } from "lucide-react";
import { useNavigate } from "react-router-dom";

const EscolhaPratos = ({ selecionados, onToggle, onVoltar, podeConcluir }) => {
  const navigate = useNavigate();

  return (
    <section className="onboarding-fase">
      <h1>Escolha seus pratos favoritos</h1>
      <p className="onboarding-subtitulo">
        Selecione pelo menos {MIN_PRATOS} pratos para finalizar seu perfil.
      </p>

      <div className="pratos-grid-circular">
        {PRATOS.map((prato) => (
          <CardPratoCirculo
            key={prato.id}
            prato={prato}
            selecionado={selecionados.includes(prato.id)}
            onToggle={() => onToggle(prato.id)}
          />
        ))}
      </div>

      <p className="onboarding-contador">
        {selecionados.length} de {MIN_PRATOS} selecionados
      </p>

      <div className="onboarding-acoes">
        <button type="button" className="botao botao-voltar" onClick={onVoltar}>
          Voltar
        </button>
        <button
          type="button"
          className="botao botao-concluir"
          onClick={() => navigate("/")}
          disabled={!podeConcluir}
        >
          <span className="botao-texto">Concluir</span>
          <ArrowRight className="botao-seta" />
        </button>
      </div>
    </section>
  );
};
export default EscolhaPratos;
