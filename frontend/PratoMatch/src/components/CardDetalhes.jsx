import "./CardDetalhes.css";
import { useState } from "react";

const CardDetalhes = ({
  titulo,
  descricao,
  imagem,
  categorias,
  tempo,
  calorias,
  numero_passos,
  passos,
  ingredientes,
  avaliações,
  estrelas,
  onAvaliar,
}) => {
  const [avaliacaoUsuario, setAvaliacaoUsuario] = useState(0);

  const renderizarEstrelas = () => {
    const total = Number(estrelas) || 0;
    return "⭐".repeat(Math.round(total));
  };

  return (
    <div className="card-detalhes">
      <div className="card-detalhes-imagem-container">
        <img className="card-detalhes-imagem" src={imagem} alt={titulo} />
      </div>

      <div className="card-detalhes-conteudo">
        <div className="card-detalhes-header">
          <h2 className="card-detalhes-titulo">{titulo}</h2>
          <div className="card-detalhes-avaliacoes-container">
            <span className="card-detalhes-estrelas">
              {renderizarEstrelas()} <span>({estrelas})</span>
            </span>
            <span className="card-detalhes-qtd-avaliacoes">
              {avaliações} avaliações
            </span>
          </div>
          <div className="card-detalhes-avaliacao-usuario">
            <span>Sua avaliação:</span>
            <div
              className="card-detalhes-estrelas-interativas"
              role="group"
              aria-label="Avalie este prato de 1 a 5 estrelas"
            >
              {[1, 2, 3, 4, 5].map((estrela) => (
                <button
                  key={estrela}
                  type="button"
                  className={estrela <= avaliacaoUsuario ? "ativa" : ""}
                  aria-label={`${estrela} estrela${estrela > 1 ? "s" : ""}`}
                  aria-pressed={estrela === avaliacaoUsuario}
                  onClick={() => {
                    setAvaliacaoUsuario(estrela);
                    onAvaliar?.(estrela);
                  }}
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
          <span className="tag categoria">{categorias}</span>
          <span className="tag tempo">⏱ {tempo}</span>
          <span className="tag calorias">🔥 {calorias} kcal</span>
        </div>

        <div className="card-detalhes-secoes">
          <div className="secao">
            <h3>🛒 Ingredientes</h3>
            <p className="texto-formatado">{ingredientes}</p>
          </div>

          <div className="secao">
            <h3>📝 Modo de Preparo ({numero_passos} passos)</h3>
            <p className="texto-formatado">{passos}</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CardDetalhes;
