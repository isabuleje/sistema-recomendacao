import { useEffect, useMemo, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { ChevronLeft, ChevronRight } from "lucide-react";

import Card from "./Card.jsx";

import { imagemAleatoria } from "../../utils/imagensPratos.js";
import { POR_PAGINA_BUSCA } from "../../constants/busca.js";

/*
  O CardGrid é responsável por exibir uma grade de cards de pratos
  Ele pode ser usado tanto com paginação local (quando todos os pratos
  já estão carregados) quanto com paginação do servidor (quando a API
  retorna apenas uma página de pratos por vez)

 */
function CardGrid({
  pratos,
  paginaAtual: paginaExterna,
  totalPaginas: totalExterno,
  onMudarPagina,
  favoritos = new Set(),
  onToggleFavorite,
}) {
  const navigate = useNavigate();

  const [paginaInterna, setPaginaInterna] = useState(1);

  // referencia para voltar ao topo do grid quando a paginação muda
  const topoRef = useRef(null);

  //a requsição de paginação do servidor é opcional, então verificamos se a função foi passada como prop
  const usaPaginacaoDoServidor = typeof onMudarPagina === "function";

  //quando a lista de pratos muda, resetamos a paginação interna para 1, caso não esteja usando paginação do servidor
  useEffect(() => {
    if (!usaPaginacaoDoServidor) {
      setPaginaInterna(1);
    }
  }, [pratos, usaPaginacaoDoServidor]);

  const paginaAtual = usaPaginacaoDoServidor ? paginaExterna : paginaInterna;

  const totalPaginas = usaPaginacaoDoServidor
    ? totalExterno
    : Math.max(1, Math.ceil(pratos.length / POR_PAGINA_BUSCA));

  //os pratos já vem "cortados" do backend
  const pratosVisiveis = usaPaginacaoDoServidor
    ? pratos
    : pratos.slice(
        (paginaAtual - 1) * POR_PAGINA_BUSCA,
        paginaAtual * POR_PAGINA_BUSCA,
      );

  // Aq resolve aquele problema de ficar renderizando as imagens o tempo todo kkkkk
  const imagens = useMemo(() => {
    return pratosVisiveis.map(() => imagemAleatoria());
  }, [pratosVisiveis]);

  const irParaPagina = (numero) => {
    if (usaPaginacaoDoServidor) {
      onMudarPagina(numero);
    } else {
      setPaginaInterna(numero);
    }
    topoRef.current?.scrollIntoView({
      behavior: "smooth",
      block: "start",
    });
  };

  return (
    <>
      <div ref={topoRef} className="cards-grid">
        {pratosVisiveis.map((prato, index) => (
          <Card
            key={prato.id}
            image={imagens[index]}
            title={prato.nome}
            description={prato.descricao || "Sem descrição disponível."}
            category={prato.tags?.length > 0 ? prato.tags[0] : "Prato"}
            prepTime={prato.tempo_preparo}
            rating={prato.estrelas}
            evaluations={prato.avaliacoes}
            isFavorite={favoritos.has(prato.id)}
            onToggleFavorite={() => onToggleFavorite?.(prato.id)}
            onOpenDetalhes={() =>
              navigate(`/pratos/${prato.id}`, {
                state: { prato },
              })
            }
          />
        ))}
      </div>

      {totalPaginas > 1 && (
        <nav className="paginacao" aria-label="Paginação de pratos">
          <button
            type="button"
            className="paginacao-botao"
            onClick={() => irParaPagina(paginaAtual - 1)}
            disabled={paginaAtual === 1}
            aria-label="Página anterior"
          >
            <ChevronLeft size={18} />
          </button>

          <span className="paginacao-info">
            Página {paginaAtual} de {totalPaginas}
          </span>

          <button
            type="button"
            className="paginacao-botao"
            onClick={() => irParaPagina(paginaAtual + 1)}
            disabled={paginaAtual === totalPaginas}
            aria-label="Próxima página"
          >
            <ChevronRight size={18} />
          </button>
        </nav>
      )}
    </>
  );
}

export default CardGrid;
