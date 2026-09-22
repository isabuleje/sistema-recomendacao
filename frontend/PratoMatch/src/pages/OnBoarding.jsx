/*
  OnBoarding — fluxo de 3 fases:
  1. Restrição alimentar / alergia
  2. Culinárias favoritas
  3. Pratos favoritos (formato circular, mínimo 3 selecionados)

*/
import { useState } from "react";
import "../components/OnBoarding/OnBoarding.css";

const RESTRICOES = [
  { value: "nenhuma", label: "Nenhuma" },
  { value: "vegetariano", label: "Vegetariano" },
  { value: "vegano", label: "Vegano" },
  { value: "gluten", label: "Sem Glúten" },
  { value: "lactose", label: "Sem Lactose" },
];

const CULINARIAS = [
  "Docinhos",
  "Bolos",
  "Almoço",
  "Jantar",
  "Sobremesa",
  "Café da manhã",
];


const PRATOS = [
  { id: "prato1", nome: "Pizza Margherita", imagem: "/Pratos/prato1.webp" },
  { id: "prato2", nome: "Sushi Tradicional", imagem: "/Pratos/prato2.webp" },
  { id: "prato3", nome: "Hambúrguer Artesanal", imagem: "/Pratos/prato3.webp" },
  { id: "prato4", nome: "Lasanha de Berinjela", imagem: "/Pratos/prato4.webp" },
  { id: "prato5", nome: "Salada Caesar", imagem: "/Pratos/prato5.webp" },
  { id: "prato6", nome: "Risoto de Cogumelos", imagem: "/Pratos/prato6.webp" },
];

const TOTAL_FASES = 3;
const MIN_PRATOS = 3;

const OnBoarding = ({ onConcluir }) => {
  const [fase, setFase] = useState(1);
  const [restricao, setRestricao] = useState("nenhuma");
  const [alergia, setAlergia] = useState("");
  const [culinariasSelecionadas, setCulinariasSelecionadas] = useState([]);
  const [pratosSelecionados, setPratosSelecionados] = useState([]);

  const toggleCulinaria = (item) => {
    setCulinariasSelecionadas((atual) =>
      atual.includes(item) ? atual.filter((c) => c !== item) : [...atual, item]
    );
  };

  const togglePrato = (id) => {
    setPratosSelecionados((atual) =>
      atual.includes(id) ? atual.filter((p) => p !== id) : [...atual, id]
    );
  };

  const avancar = () => setFase((f) => Math.min(f + 1, TOTAL_FASES));
  const voltar = () => setFase((f) => Math.max(f - 1, 1));

  const podeAvancarFase2 = culinariasSelecionadas.length > 0;
  const podeConcluir = pratosSelecionados.length >= MIN_PRATOS;

  const handleConcluir = () => {
    const preferencias = {
      restricao,
      alergia,
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
        <header className="onboarding-header">
          <span className="onboarding-logo">🍽️ PratoMatch</span>

          <div className="onboarding-progresso" role="list" aria-label={`Fase ${fase} de ${TOTAL_FASES}`}>
            {[1, 2, 3].map((n) => (
              <span
                key={n}
                role="listitem"
                className={
                  "progresso-ponto" +
                  (n === fase ? " ativo" : "") +
                  (n < fase ? " concluido" : "")
                }
              />
            ))}
          </div>

          <span className="onboarding-fase-label">
            Fase {fase} de {TOTAL_FASES}
          </span>
        </header>

        {fase === 1 && (
          <RestricaoAlimentar
            restricao={restricao}
            setRestricao={setRestricao}
            alergia={alergia}
            setAlergia={setAlergia}
            onAvancar={avancar}
          />
        )}

        {fase === 2 && (
          <EscolhaCulinaria
            selecionadas={culinariasSelecionadas}
            onToggle={toggleCulinaria}
            onVoltar={voltar}
            onAvancar={avancar}
            podeAvancar={podeAvancarFase2}
          />
        )}

        {fase === 3 && (
          <EscolhaPratos
            selecionados={pratosSelecionados}
            onToggle={togglePrato}
            onVoltar={voltar}
            onConcluir={handleConcluir}
            podeConcluir={podeConcluir}
          />
        )}
      </div>
    </section>
  );
};

const RestricaoAlimentar = ({ restricao, setRestricao, alergia, setAlergia, onAvancar }) => {
  return (
    <section className="onboarding-fase">
      <h1 style={{ fontSize: "2rem", fontWeight: "700", color: "var(--verde-escuro)" }}>Antes de começar, conte-nos sobre sua alimentação</h1>
      <p className="onboarding-subtitulo">
        Assim, as recomendações ficam mais seguras e do seu estilo de vida.
      </p>

      <div className="campo">
        <label htmlFor="restricao">Você tem alguma restrição alimentar?</label>
        <select
          name="restricao"
          id="restricao"
          value={restricao}
          onChange={(e) => setRestricao(e.target.value)}
        >
          {RESTRICOES.map((r) => (
            <option key={r.value} value={r.value}>
              {r.label}
            </option>
          ))}
        </select>
      </div>

      <div className="campo">
        <label htmlFor="alergia">Você possui algum tipo de alergia?</label>
        <input
          id="alergia"
          type="text"
          placeholder="Ex: amendoim, camarão..."
          value={alergia}
          onChange={(e) => setAlergia(e.target.value)}
        />
      </div>

      <p className="onboarding-nota">
        Você pode alterar essas escolhas depois no seu perfil.
      </p>

      <div className="onboarding-acoes onboarding-acoes-unica">
        <button type="button" className="botao botao-primario" onClick={onAvancar}>
          Continuar
        </button>
      </div>
    </section>
  );
};

const EscolhaCulinaria = ({ selecionadas, onToggle, onVoltar, onAvancar, podeAvancar }) => {
  return (
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
        <p className="onboarding-nota">Escolha ao menos uma culinária para continuar.</p>
      )}

      <div className="onboarding-acoes">
        <button type="button" className="botao botao-secundario" onClick={onVoltar}>
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
};

const EscolhaPratos = ({ selecionados, onToggle, onVoltar, onConcluir, podeConcluir }) => {
  return (
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
        <button type="button" className="botao botao-secundario" onClick={onVoltar}>
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
};

const CardPratoCirculo = ({ prato, selecionado, onToggle }) => {
  return (
    <button
      type="button"
      className={"prato-circulo" + (selecionado ? " prato-circulo-ativo" : "")}
      aria-pressed={selecionado}
      onClick={onToggle}
    >
      <span className="prato-circulo-imagem">
        <img src={prato.imagem} alt="" />
        {selecionado && <span className="prato-circulo-check">✓</span>}
      </span>
      <span className="prato-circulo-nome">{prato.nome}</span>
    </button>
  );
};

export default OnBoarding;
