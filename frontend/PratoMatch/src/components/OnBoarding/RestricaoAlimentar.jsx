import { RESTRICOES } from "./onboardingData";
import { ArrowRight, Search } from "lucide-react";

const RestricaoAlimentar = ({
  restricao,
  setRestricao,
  alergia,
  setAlergia,
  alergias,
  adicionarAlergia,
  removerAlergia,
  onAvancar,
  ingredientes,
}) => {
  const sugestoes = ingredientes
    .filter((ingrediente) =>
      ingrediente.toLowerCase().includes(alergia.toLowerCase()),
    )
    .filter((ingrediente) => !alergias.includes(ingrediente));

  return (
    <section className="onboarding-fase">
      <h1>Antes de começar, conte-nos sobre sua alimentação</h1>
      <p className="onboarding-subtitulo">
        Assim, as recomendações ficam mais seguras e do seu estilo de vida.
      </p>

      <div className="titulo-grupo">
        <div className="titulo-com-icone">
          <img
            src="public/leaf (1).png"
            width={40}
            height={40}
            alt="Ícone de folha"
            className="alert-icon"
          />
          <h2 className="campo-subtitulo">
            Você possui alguma restrição alimentar?
          </h2>
        </div>

        <p className="campo-complemento">
          Selecione todas as opções que se aplicam a você. Se não houver
          nenhuma, selecione "Nenhuma".
        </p>
      </div>

      <div
        className="listaCampos"
        role="radiogroup"
        aria-label="Restrição alimentar"
      >
        {RESTRICOES.map((opcao) => (
          <label className="campo" key={opcao.value}>
            <input
              type="radio"
              name="restricao"
              value={opcao.value}
              className="campoCheckbox"
              checked={restricao === opcao.value}
              onChange={() => setRestricao(opcao.value)}
            />
            <span className="campoIcone" aria-hidden="true">
              {opcao.icone}
            </span>
            <span className="campoNome">{opcao.label}</span>
            <span className="campoDescricao">{opcao.descricao}</span>
            <span className="campoCheck" aria-hidden="true">
              ✓
            </span>
          </label>
        ))}
      </div>

      <div className="titulo-grupo">
        <div className="titulo-com-icone">
          <img
            src="public/alert.png"
            alt="Ícone de alerta"
            width={40}
            height={40}
          />
          <h2 className="campo-subtitulo">Você possui alguma alergia?</h2>
        </div>

        <label htmlFor="alergia" className="campo-label">
          Informe se há algum elemento que você não pode consumir
        </label>
      </div>

      <div className="campo campo-alergia">
        <div className="autocomplete">
          <Search className="search-icon" />
          <input
            id="alergia"
            type="text"
            placeholder="Ex: amendoim, camarão..."
            value={alergia}
            onChange={(event) => setAlergia(event.target.value)}
          />

          {alergia && sugestoes.length > 0 && (
            <div className="sugestoes">
              {sugestoes.map((ingrediente) => (
                <button
                  type="button"
                  key={ingrediente}
                  onClick={() => adicionarAlergia(ingrediente)}
                >
                  {ingrediente}
                </button>
              ))}
            </div>
          )}
        </div>
        <div className="tagsAlergias" aria-live="polite">
          {alergias.map((ingrediente) => (
            <span className="tagAlergia" key={ingrediente}>
              {ingrediente}
              <button
                type="button"
                aria-label={`Remover ${ingrediente}`}
                onClick={() => removerAlergia(ingrediente)}
              >
                ×
              </button>
            </span>
          ))}
        </div>
      </div>

      <p className="onboarding-nota">
        <img
          src="public/letter-i.png"
          alt="Ícone de alerta"
          width={20}
          height={20}
        />
        Você pode alterar essas escolhas depois no seu perfil.
      </p>
      
      <div className="onboarding-acoes onboarding-acoes-unica">
        <button
          type="button"
          className="botao botao-primario"
          onClick={onAvancar}
        >
          <span className="botao-texto">Continuar</span>
          <ArrowRight className="botao-seta" />
        </button>
      </div>
    </section>
  );
};

export default RestricaoAlimentar;
