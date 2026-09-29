// Página inicial, onde o usuário vai poder ver os pratos recomendados

import "../components/Home/Placa.css";
import "../components/Home/Categorias.css";
import "../components/Home/Input.css";

import { Search, Send, ChevronLeft, ChevronRight } from "lucide-react";

import Card from "../components/Home/Card";
import FilterSection from "../components/Home/Filtro.jsx";
import Loading from "../components/Loading/Loading.jsx";

import { useEffect, useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import {
  buscarPratoFavoritados,
  buscarRecomendados,
  salvarFavoritos,
} from "../services/Pratos.js";
import { useBuscaPratos, POR_PAGINA_BUSCA } from "../hooks/useBuscaPratos.js";

const ITENS_POR_PAGINA = 24;

const CategorySection = ({
  title,
  description,
  pratos,
  paginaAtual,
  totalPaginas,
  onMudarPagina,
  favoritos,
  onToggleFavorite,
}) => (
  <section className="category-section">
    <div className="category-heading">
      <h2 className="category-title" style={{ color: "#055746" }}>
        {title}
      </h2>

      <p>{description}</p>
    </div>

    <CardGrid
      pratos={pratos}
      paginaAtual={paginaAtual} //temos páginas :D e nem demora pra carregar
      totalPaginas={totalPaginas}
      onMudarPagina={onMudarPagina}
      favoritos={favoritos}
      onToggleFavorite={onToggleFavorite}
    />
  </section>
);

const CardGrid = ({
  pratos,
  paginaAtual: paginaExterna,
  totalPaginas: totalExterno,
  onMudarPagina,
  favoritos = new Set(),
  onToggleFavorite,
}) => {
  const navigate = useNavigate();
  const [paginaInterna, setPaginaInterna] = useState(1);
  const topoRef = useRef(null); //pra rolar pro topo da lista de pratos quando mudar de página

  // true quando a paginação é feita pela API (busca)
  const servidor = onMudarPagina !== undefined;

  // no modo local, volta para a página 1 se a lista mudar
  useEffect(() => {
    if (!servidor) setPaginaInterna(1);
  }, [pratos, servidor]);

  const paginaAtual = servidor ? paginaExterna : paginaInterna;
  const totalPaginas = servidor
    ? totalExterno
    : Math.max(1, Math.ceil(pratos.length / ITENS_POR_PAGINA));

  // na API a lista já vem cortada
  const pratosVisiveis = servidor
    ? pratos
    : pratos.slice(
        (paginaAtual - 1) * ITENS_POR_PAGINA,
        paginaAtual * ITENS_POR_PAGINA,
      );

  const irParaPagina = (numero) => {
    (servidor ? onMudarPagina : setPaginaInterna)(numero);
    topoRef.current?.scrollIntoView({ behavior: "smooth", block: "start" });
  };

  return (
    <>
      <div ref={topoRef} className="cards-grid">
        {pratosVisiveis.map((prato) => (
          <Card
            key={prato.id}
            image="public/Pratos/pizzar.jpg"
            title={prato.nome}
            description={prato.descricao || "Sem descrição disponível."}
            category={prato.tags?.length > 0 ? prato.tags[0] : "Prato"}
            prepTime={prato.tempo_preparo}
            rating={prato.estrelas}
            evaluations={prato.avaliacoes}
            isFavorite={favoritos.has(prato.id)}
            onToggleFavorite={() => onToggleFavorite?.(prato.id)}
            onOpenDetalhes={() =>
              navigate(`/pratos/${prato.id}`, { state: { prato } })
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
};

const Home = () => {
  const [pratos, setPratos] = useState([]);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState(null);
  const [favoritos, setFavoritos] = useState(new Set());

  const [termoBusca, setTermoBusca] = useState("");
  const [paginaBusca, setPaginaBusca] = useState(1);

  const { resultados, total, buscando, erroBusca, emBusca } = useBuscaPratos(
    termoBusca,
    paginaBusca,
  );

  const totalPaginasBusca = Math.max(1, Math.ceil(total / POR_PAGINA_BUSCA));

  useEffect(() => {
    const carregarPratos = async () => {
      try {
        setCarregando(true);
        setErro(null);

        const dados = await buscarRecomendados();
        setPratos(dados);
      } catch (error) {
        console.error("Erro ao carregar pratos:", error);

        setErro("Não foi possível carregar os pratos.");
      } finally {
        setCarregando(false);
      }
    };

    carregarPratos();
  }, []);

  useEffect(() => {
    buscarPratoFavoritados()
      .then((dados) => setFavoritos(new Set(dados.map((prato) => prato.id))))
      .catch((error) => console.error("Erro ao carregar favoritos:", error));
  }, []);

  const alternarFavorito = async (pratoId) => {
    const eraFavorito = favoritos.has(pratoId);
    setFavoritos((atuais) => {
      const atualizados = new Set(atuais);
      eraFavorito ? atualizados.delete(pratoId) : atualizados.add(pratoId);
      return atualizados;
    });

    try {
      await salvarFavoritos(pratoId, !eraFavorito);
    } catch (error) {
      setFavoritos((atuais) => {
        const revertidos = new Set(atuais);
        eraFavorito ? revertidos.add(pratoId) : revertidos.delete(pratoId);
        return revertidos;
      });
      console.error("Erro ao atualizar favorito:", error);
    }
  };

  return (
    <div className="home-page">
      <div className="user-greeting">
        <p
          style={{
            color: "#055746",
            fontWeight: "700",
          }}
        >
          Olá, usuário! 👋
        </p>

        <i className="bx bx-user" style={{ color: "#000504" }} />
      </div>

      <div className="placa">
        <div className="placa-conteudo">
          <h2 className="placa-texto">Encontre o prato perfeito para você</h2>

          <p className="placa-subtitulo">
            Descubra novas opções com base nos seus gostos e preferências.
          </p>
        </div>
      </div>

      <section className="home-content">
        <div className="category-filter-row">
          <div className="input-wrapper">
            <Search className="search-icon" />

            <input
              type="text"
              placeholder="O que você quer comer hoje?"
              name="text"
              className="input"
              value={termoBusca}
              onChange={(e) => {
                setTermoBusca(e.target.value);
                setPaginaBusca(1);
              }}
            />

            {termoBusca && (
              <button
                className="send-button"
                type="button"
                aria-label="Limpar pesquisa"
                onClick={() => {
                  setTermoBusca("");
                  setPaginaBusca(1);
                }}
              >
                <Send />
              </button>
            )}
          </div>

          {!emBusca && <FilterSection />}
        </div>

        {emBusca ? (
          <>
            {/* loading só na primeira carga; ao trocar de página a lista antiga fica visível */}
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

            {!erroBusca && (resultados.length > 0 || !buscando) && (
              <CategorySection
                title={`Resultados para "${termoBusca}"`}
                description={
                  total > 0
                    ? `${total} prato(s) encontrado(s).`
                    : "Nenhum prato encontrado com esse termo."
                }
                pratos={resultados}
                paginaAtual={paginaBusca}
                totalPaginas={totalPaginasBusca}
                onMudarPagina={setPaginaBusca}
                favoritos={favoritos}
                onToggleFavorite={alternarFavorito}
              />
            )}
          </>
        ) : (
          <>
            {carregando && (
              <div className="pratos-loading">
                <Loading />
              </div>
            )}

            {!carregando && erro && (
              <div className="pratos-error">
                <p>{erro}</p>
              </div>
            )}

            {!carregando && !erro && (
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
