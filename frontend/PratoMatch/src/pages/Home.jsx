import { Search, Send } from "lucide-react";

import "../components/Home/Placa.css";
import "../components/Home/Categorias.css";
import "../components/Home/Input.css";

import CategorySection from "../components/Home/CategorySection.jsx";
import Loading from "../components/Loading/Loading.jsx";

import { useBuscaPratos } from "../hooks/useBuscaPratos.js";
import { useFavoritos } from "../hooks/useFavoritos.js";
import { usePerfil } from "../hooks/usePerfil.js";
import { useRecomendacoes } from "../hooks/useRecomendacoes.js";

const Home = () => {
  const { perfil } = usePerfil();
  const {
    pratos,
    carregando: carregandoRecomendacoes,
    erro: erroRecomendacoes,
  } = useRecomendacoes();
  const { favoritos, alternarFavorito } = useFavoritos();

  const {
    termo,
    alterarBusca,
    limparBusca,

    pagina,
    mudarPagina,

    resultados,
    total,

    buscando,
    erro: erroBusca,

    emBusca,
    totalPaginas,
  } = useBuscaPratos();

  return (
    <div className="home-page">
      {/* Cabeçalho */}

      <div className="user-greeting">
        <p>Olá, {perfil?.username ?? "usuário"}! 👋</p>

        <i className="bx bx-user" aria-hidden="true" />
      </div>

      {/* Placa principal */}

      <div className="placa">
        <div className="placa-conteudo">
          <h2 className="placa-texto">Encontre o prato perfeito para você</h2>

          <p className="placa-subtitulo">
            Descubra novas opções com base nos seus gostos e preferências.
          </p>
        </div>
      </div>

      {/* Conteúdo da home */}
      <section className="home-content">
        {/* Barra de pesquisa*/}

        <div className="category-filter-row">
          <div className="input-wrapper">
            <Search className="search-icon" aria-hidden="true" />

            <input
              type="text"
              placeholder="O que você quer comer hoje?"
              name="text"
              className="input"
              value={termo}
              onChange={alterarBusca}
              aria-label="Pesquisar pratos"
            />

            {termo && (
              <button
                className="send-button"
                type="button"
                aria-label="Limpar pesquisa"
                onClick={limparBusca}
              >
                <Send />
              </button>
            )}
          </div>
        </div>

        {/* Resulados da busca */}

        {emBusca ? (
          <>
            {buscando && resultados.length === 0 && (
              <div className="pratos-loading">
                <Loading />
              </div>
            )}

            {!buscando && erroBusca && (
              <div className="pratos-error">
                <p>{erroBusca}</p>
              </div>
            )}

            {!erroBusca && (
              <CategorySection
                title={`Resultados para "${termo}"`}
                description={
                  total > 0
                    ? `${total} prato(s) encontrado(s).`
                    : "Nenhum prato encontrado com esse termo."
                }
                pratos={resultados}
                paginaAtual={pagina}
                totalPaginas={totalPaginas}
                onMudarPagina={mudarPagina}
                favoritos={favoritos}
                onToggleFavorite={alternarFavorito}
              />
            )}
          </>
        ) : (
          <>
            {/* Recomendacoes */}

            {carregandoRecomendacoes && (
              <div className="pratos-loading">
                <Loading />
              </div>
            )}

            {!carregandoRecomendacoes && erroRecomendacoes && (
              <div className="pratos-error">
                <p>{erroRecomendacoes}</p>
              </div>
            )}

            {!carregandoRecomendacoes && !erroRecomendacoes && (
              <CategorySection
                title="Recomendados para você"
                description="Encontre os pratos mais indicados para o seu gosto."
                pratos={pratos}
                favoritos={favoritos}
                onToggleFavorite={alternarFavorito}
              />
            )}
          </>
        )}
      </section>
    </div>
  );
};

export default Home;
