import { useState } from "react";
import { ArrowRight } from "lucide-react";

const EscolhaCulinaria = ({
  selecionadas,
  onToggle,
  onVoltar,
  onAvancar,
  podeAvancar,
  categorias,
}) => {
  const CATEGORIAS_POR_VEZ = 109;

  const [pagina, setPagina] = useState(0);

  // Quantidade de grupos de categorias
  const totalPaginas = Math.ceil(categorias.length / CATEGORIAS_POR_VEZ);

  // Garante que a página nunca fique fora do limite
  const paginaAtual = totalPaginas > 0 ? pagina % totalPaginas : 0;

  // Categorias que serão exibidas
  const inicio = paginaAtual * CATEGORIAS_POR_VEZ;

  const categoriasVisiveis = categorias.slice(
    inicio,
    inicio + CATEGORIAS_POR_VEZ,
  );

  const mostrarOutras = () => {
    setPagina((paginaAnterior) => {
      if (totalPaginas === 0) {
        return 0;
      }

      return (paginaAnterior + 1) % totalPaginas;
    });
  };

  return (
    <section className="onboarding-fase">
      <div className="titulo-linha">
        <h1>Escolha suas culinárias favoritas</h1>

        {totalPaginas > 1 && (
          <button
            type="button"
            className="botao botao-secundario botao-refresh"
            onClick={mostrarOutras}
          >
            <span>↻</span>
            <span>Mostrar outras</span>
          </button>
        )}
      </div>

      <p className="onboarding-subtitulo">
        Assim, as recomendações ficam mais personalizadas ao seu estilo de vida.
      </p>

      <div className="chips-grid">
        {categoriasVisiveis.map((item) => {
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
          <img
            src="/letter-i.png"
            alt="Ícone de alerta"
            width={20}
            height={20}
          />
          Escolha pelo menos uma culinária para continuar.
        </p>
      )}

      <div className="onboarding-acoes">
        <button
          type="button"
          className="botao botao-secundario"
          onClick={onVoltar}
          style={{ height: "2.7rem" }}
        >
          Voltar
        </button>

        <button
          type="button"
          className="botao botao-primario"
          onClick={onAvancar}
          disabled={!podeAvancar}
          style={{ height: "2.7rem" }}
        >
          <span className="botao-texto">Continuar</span>
          <ArrowRight className="botao-seta" />
        </button>
      </div>
    </section>
  );
};

export default EscolhaCulinaria;
