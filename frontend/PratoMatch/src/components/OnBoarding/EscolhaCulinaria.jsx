import { CULINARIAS } from "./onboardingData";

const EscolhaCulinaria = ({
  selecionadas,
  onToggle,
  onVoltar,
  onAvancar,
  podeAvancar,
}) => (
  <section className="onboarding-fase">
    <h2>Escolha suas culinárias favoritas</h2>
    <p className="onboarding-subtitulo">
      Assim, as recomendações ficam mais personalizadas ao seu estilo de vida.
    </p>

    <div className="chips-grid">
      {CULINARIAS.map((item) => {
        const ativo = selecionadas.includes(item);
        return (
          <button
            key={item}
            type="button"
            className={"chip" + (ativo ? " chip-ativo" : "")}
            aria-pressed={ativo}
            onClick={() => onToggle(item)}
          >
            {item}
          </button>
        );
      })}
    </div>

    {!podeAvancar && (
      <p className="onboarding-nota">
        Escolha ao menos uma culinária para continuar.
      </p>
    )}

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
        onClick={onAvancar}
        disabled={!podeAvancar}
      >
        Continuar
      </button>
    </div>
  </section>
);

export default EscolhaCulinaria;
