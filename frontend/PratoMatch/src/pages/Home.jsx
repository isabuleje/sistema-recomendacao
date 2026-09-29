// Página inicial, onde o usuário vai poder ver os pratos
// recomendados, populares e novidades

import "../components/Home/Placa.css";
import "../components/Home/Categorias.css";
import "../components/Home/Input.css";

import { Search, Send } from "lucide-react";

import Card from "../components/Home/Card";
import FilterSection from "../components/Home/Filtro.jsx";
import Loading from "../components/Loading/Loading.jsx";

import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { buscarPratos } from "../services/Pratos.js";
import { useBuscaPratos } from "../hooks/useBuscaPratos.js";

const CategorySection = ({ title, description, pratos }) => (
  <section className="category-section">
    <div className="category-heading">
      <h2 className="category-title" style={{ color: "#055746" }}>
        {title}
      </h2>

      <p>{description}</p>
    </div>

    <CardGrid pratos={pratos} />
  </section>
);

const ITENS_POR_PAGINA = 24;

const CardGrid = ({ pratos }) => {
  const navigate = useNavigate();
  const [quantidadeVisivel, setQuantidadeVisivel] = useState(ITENS_POR_PAGINA);

  // some se a lista de pratos mudar (ex: nova busca)
  useEffect(() => {
    setQuantidadeVisivel(ITENS_POR_PAGINA);
  }, [pratos]);

  const pratosVisiveis = pratos.slice(0, quantidadeVisivel);
  const temMais = quantidadeVisivel < pratos.length;

  return (
    <>
      <div className="cards-grid">
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
            onOpenDetalhes={() =>
              navigate(`/pratos/${prato.id}`, { state: { prato } })
            }
          />
        ))}
      </div>

      {temMais && (
        <div className="mostrar-mais-wrapper">
          <button
            type="button"
            className="mostrar-mais-botao"
            onClick={() =>
              setQuantidadeVisivel((atual) => atual + ITENS_POR_PAGINA)
            }
          >
            Mostrar mais
          </button>
        </div>
      )}
    </>
  );
};

const Home = ({ favoritos, alternarFavorito }) => {
  const [pratos, setPratos] = useState([]);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState(null);

  const [termoBusca, setTermoBusca] = useState("");
  const { resultados, buscando, erroBusca, emBusca } =
    useBuscaPratos(termoBusca);

  useEffect(() => {
    const carregarPratos = async () => {
      try {
        setCarregando(true);
        setErro(null);

        const dados = await buscarPratos();

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
              onChange={(e) => setTermoBusca(e.target.value)}
            />

            {termoBusca && (
              <button
                className="send-button"
                type="button"
                aria-label="Limpar pesquisa"
                onClick={() => setTermoBusca("")}
              >
                <Send />
              </button>
            )}
          </div>

          {!emBusca && <FilterSection />}
        </div>

        {emBusca ? (
          <>
            {buscando && (
              <div className="pratos-loading">
                <Loading />
              </div>
            )}

            {!buscando && erroBusca && (
              <div className="pratos-error">
                <p>{erroBusca}</p>
              </div>
            )}

            {!buscando && !erroBusca && (
              <CategorySection
                title={`Resultados para "${termoBusca}"`}
                description={
                  resultados.length > 0
                    ? `${resultados.length} prato(s) encontrado(s).`
                    : "Nenhum prato encontrado com esse termo."
                }
                pratos={resultados}
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
              <>
                <CategorySection
                  title="Recomendados para você"
                  description="Encontre os pratos mais indicados para o seu gosto."
                  pratos={pratos.slice(0, 20)}
                  favoritos={favoritos}
                  alternarFavorito={alternarFavorito}
                />
              </>
            )}
          </>
        )}
      </section>
    </div>
  );
};

export default Home;
