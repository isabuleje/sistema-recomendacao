import CardPratoCirculo from "../CardPratoCirculo";
import { MIN_PRATOS } from "../../../constants/onboardingData.js";
import { ArrowRight } from "lucide-react";

const EscolhaPratos = ({
  selecionados,
  pratos,
  carregando,
  onToggle,
  onVoltar,
  onConcluir,
  podeConcluir,
  salvando,
}) => {
  return (
    <section className="onboarding-fase">
      <h1>Escolha seus pratos favoritos</h1>
      <p className="onboarding-subtitulo">
        Selecione pelo menos {MIN_PRATOS} pratos para finalizar seu perfil.
      </p>

      <div className="pratos-grid-circular">
        {carregando && (
          <p className="onboarding-subtitulo">Carregando pratos...</p>
        )}
        {!carregando &&
          pratos.map((prato) => (
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
          onClick={onConcluir}
          disabled={!podeConcluir}
        >
          <span className="botao-texto">
            {salvando ? "Salvando..." : "Concluir"}
          </span>
          <ArrowRight className="botao-seta" />
        </button>
      </div>
    </section>
  );
};
export default EscolhaPratos;
