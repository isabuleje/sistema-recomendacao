import CardPratoCirculo from "./CardPratoCirculo";
import { MIN_PRATOS, PRATOS } from "./onboardingData";

const EscolhaPratos = ({
  selecionados,
  onToggle,
  onVoltar,
  onConcluir,
  podeConcluir,
}) => (
  <section className="onboarding-fase">
    <h2>Escolha seus pratos favoritos</h2>
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
      <button
        type="button"
        className="botao botao-secundario"
        onClick={onVoltar}
      >
        Voltar
      </button>
      <button
        type="button"
        className="botao botao-primario"
        onClick={onConcluir}
        disabled={!podeConcluir}
      >
        Concluir
      </button>
    </div>
  </section>
);

export default EscolhaPratos;
