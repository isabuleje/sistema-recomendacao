import "./CardDetalhes.css";
import { useState } from "react";

const normalizarLista = (valor) => {
  if (Array.isArray(valor)) {
    return valor.filter(
      (item) => item !== null && item !== undefined && item !== "",
    );
  }
  if (typeof valor === "string") {
    return valor
      .split(/\r?\n|,/)
      .map((item) => item.trim())
      .filter(Boolean);
  }
  return [];
};

const dividirEmDuasColunas = (lista) => {
  const metade = Math.ceil(lista.length / 2);
  return [lista.slice(0, metade), lista.slice(metade)];
};

const CardDetalhes = ({
  titulo,
  descricao,
  imagem,
  categorias,
  tempo,
  tempoVisualizado = 0,
  ingredientes,
  passos,
  avaliacoes = 0,
  estrelas = 0,
  avaliacaoUsuario: avaliacaoUsuarioProp,
  salvando,
  onAvaliar,
}) => {
  const [avaliacaoInterna, setAvaliacaoInterna] = useState(0);
  const avaliacaoUsuario =
    avaliacaoUsuarioProp !== undefined
      ? avaliacaoUsuarioProp
      : avaliacaoInterna;

  const listaIngredientes = normalizarLista(ingredientes);
  const listaPassos = normalizarLista(passos);
  const [colunaEsquerdaPassos, colunaDireitaPassos] =
    dividirEmDuasColunas(listaPassos);

  const categoriasCompletas = normalizarLista(categorias);
  const listaCategorias = categoriasCompletas.slice(0, 5);

  const mediaEstrelas = Number(estrelas) || 0;
  const estrelasCheias = Math.round(mediaEstrelas);

  const handleAvaliar = (nota) => {
    if (avaliacaoUsuarioProp === undefined) setAvaliacaoInterna(nota);
    onAvaliar?.(nota);
  };

  //deve ter alguma biblioteca pra isso, mas o google me deu logo essas formulas quando eu perguntei ent da pra usar
  const temTempo = tempo !== undefined && tempo !== null && tempo !== "";
  const segundosVisualizados = Math.max(0, Number(tempoVisualizado) || 0);
  const horas = Math.floor(segundosVisualizados / 3600);
  const minutos = Math.floor((segundosVisualizados % 3600) / 60);
  const segundos = segundosVisualizados % 60;
  const doisDigitos = (valor) => String(valor).padStart(2, "0");
  const tempoFormatado =
    horas > 0
      ? `${horas}:${doisDigitos(minutos)}:${doisDigitos(segundos)}`
      : `${doisDigitos(minutos)}:${doisDigitos(segundos)}`;


  const renderizarPasso = (passo, indiceReal) => (
    <li className="passo-item" key={`${passo}-${indiceReal}`}>
      <span className="passo-numero">
        {String(indiceReal + 1).padStart(2, "0")}
      </span>
      <span className="passo-texto">{passo}</span>
    </li>
  );

  return (
    <div className="card-detalhes-pagina">
      <div className="card-detalhes-corpo">
        <div className="card-detalhes-principal">
          <div className="card-detalhes-imagem-container">
            <img className="card-detalhes-imagem" src={imagem} alt={titulo} />
          </div>

          <div className="card-detalhes-conteudo">
            <div className="card-detalhes-header">
              <h1 className="card-detalhes-titulo">{titulo}</h1>

              <div className="card-detalhes-avaliacoes-container">
                <span className="card-detalhes-estrelas">
                  {"★".repeat(estrelasCheias)}
                  {"☆".repeat(Math.max(0, 5 - estrelasCheias))}{" "}
                  <span>({mediaEstrelas})</span>
                </span>
                <span className="card-detalhes-qtd-avaliacoes">
                  {avaliacoes} avaliaç{avaliacoes === 1 ? "ão" : "ões"}
                </span>
              </div>

              <div
                className="card-detalhes-tempo-visualizado"
                aria-live="polite"
              >
                <span>Tempo visualizado</span>
                <span className="card-detalhes-tempo-valor">{tempoFormatado}</span>
              </div>

              <div className="card-detalhes-avaliacao-usuario">
                <span style={{ fontWeight: "600" }}>Sua avaliação:</span>
                <div
                  className="card-detalhes-estrelas-interativas"
                  role="group"
                  aria-label="Avalie este prato de 1 a 5 estrelas"
                >
                  {[1, 2, 3, 4, 5].map((estrela) => (
                    <button
                      key={estrela}
                      type="button"
                      disabled={salvando}
                      className={estrela <= avaliacaoUsuario ? "ativa" : ""}
                      aria-label={`${estrela} estrela${estrela > 1 ? "s" : ""}`}
                      aria-pressed={estrela === avaliacaoUsuario}
                      onClick={() => handleAvaliar(estrela)}
                    >
                      ★
                    </button>
                  ))}
                </div>
                {avaliacaoUsuario > 0 && (
                  <span className="card-detalhes-avaliacao-confirmada">
                    {avaliacaoUsuario}/5
                  </span>
                )}
              </div>
            </div>

            <p className="card-detalhes-descricao">{descricao}</p>

            <div className="card-detalhes-tags">
              {listaCategorias.map((categoria) => (
                <span className="tag categoria" key={categoria}>
                  🍲 {categoria}
                </span>
              ))}
              {temTempo && (
                <span className="tag tempo">
                  🕜 {typeof tempo === "number" ? `${tempo} min` : tempo}
                </span>
              )}
            </div>
          </div>
        </div>

        <div className="card-secao card-secao--ingredientes">
          <h3 className="card-secao-titulo">🛒 Ingredientes</h3>
          <ul className="ingredientes-grid">
            {listaIngredientes.map((ingrediente, indice) => (
              <li className="ingrediente-item" key={`${ingrediente}-${indice}`}>
                <span className="ingrediente-check" aria-hidden="true">
                  ✓
                </span>
                {ingrediente}
              </li>
            ))}
          </ul>
        </div>

        <div className="card-secao card-secao--passos">
          <div className="card-secao-cabecalho">
            <h3 className="card-secao-titulo">📝 Modo de Preparo</h3>
            <span className="badge-passos">
              {listaPassos.length} passo{listaPassos.length === 1 ? "" : "s"}
            </span>
          </div>

          <div className="passos-colunas">
            <ol className="passos-coluna" start={1}>
              {colunaEsquerdaPassos.map((passo, indice) =>
                renderizarPasso(passo, indice),
              )}
            </ol>
            <ol className="passos-coluna">
              {colunaDireitaPassos.map((passo, indice) =>
                renderizarPasso(passo, colunaEsquerdaPassos.length + indice),
              )}
            </ol>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CardDetalhes;
