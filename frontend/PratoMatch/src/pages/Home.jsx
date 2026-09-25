// Página inicial, onde o usuário vai poder ver os pratos
// recomendados, populares e novidades

import "../components/Home/Placa.css";
import "../components/Home/Categorias.css";
import "../components/Home/Input.css";

import { Search, Send } from "lucide-react";

import Card from "../components/Home/Card";
import FilterSection from "../components/Home/Filtro.jsx";
import Loading from "../components/Loading/Loading.jsx";

import { useEffect, useRef, useState } from "react";
import { buscarPratos } from "../services/Pratos.js";

const CategorySection = ({
  title,
  description,
  pratos,
  favoritos,
  alternarFavorito,
}) => (
  <section className="category-section">
    <div className="category-heading">
      <h2 className="category-title" style={{ color: "#055746" }}>
        {title}
      </h2>

      <p>{description}</p>
    </div>

    <CardRail
      pratos={pratos}
      favoritos={favoritos}
      alternarFavorito={alternarFavorito}
    />
  </section>
);

const CardRail = ({ pratos, favoritos, alternarFavorito }) => {
  const cardsRef = useRef(null);

  const dragState = useRef({
    isDragging: false,
    startX: 0,
    startScrollLeft: 0,
  });

  // Começa o arraste
  const handlePointerDown = (event) => {
    if (event.pointerType === "mouse" && event.button !== 0) {
      return;
    }

    const container = cardsRef.current;

    if (!container) {
      return;
    }

    dragState.current = {
      isDragging: true,
      startX: event.clientX,
      startScrollLeft: container.scrollLeft,
    };

    container.setPointerCapture(event.pointerId);

    container.classList.add("is-dragging");
  };

  // Durante o arraste
  const handlePointerMove = (event) => {
    if (!dragState.current.isDragging) {
      return;
    }

    const container = cardsRef.current;

    if (!container) {
      return;
    }

    const distance = event.clientX - dragState.current.startX;

    container.scrollLeft = dragState.current.startScrollLeft - distance;
  };

  // Para o arraste
  const stopDragging = (event) => {
    if (!dragState.current.isDragging) {
      return;
    }

    const container = cardsRef.current;

    dragState.current.isDragging = false;

    if (container) {
      container.releasePointerCapture?.(event.pointerId);

      container.classList.remove("is-dragging");
    }
  };

  return (
    <div className="card-rail">
      <div
        className="cards-container"
        ref={cardsRef}
        onPointerDown={handlePointerDown}
        onPointerMove={handlePointerMove}
        onPointerUp={stopDragging}
        onPointerCancel={stopDragging}
        onPointerLeave={stopDragging}
      >
        {pratos.map((prato) => (
          <Card
            key={prato.id}
            image="public/Pratos/pizzar.jpg"
            title={prato.nome}
            description={prato.descricao || "Sem descrição disponível."}
            category={prato.tags?.length > 0 ? prato.tags[0] : "Prato"}
            prepTime={prato.tempo_preparo}
            rating={prato.estrelas}
            evaluations={prato.avaliacoes}
            isFavorite={favoritos.some((favorito) => favorito.id === prato.id)}
            onToggleFavorite={() => alternarFavorito(prato)}
          />
        ))}
      </div>
    </div>
  );
};

const Home = ({ favoritos, alternarFavorito }) => {
  const [pratos, setPratos] = useState([]);
  const [carregando, setCarregando] = useState(true);

  const [erro, setErro] = useState(null);

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
            />

            <button
              className="send-button"
              type="button"
              aria-label="Pesquisar"
            >
              <Send />
            </button>
          </div>

          <FilterSection />
        </div>

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
              pratos={pratos.slice(0, 10)}
              favoritos={favoritos}
              alternarFavorito={alternarFavorito}
            />

            <CategorySection
              title="Pratos populares"
              description="Os pratos mais pedidos pelos nossos usuários."
              pratos={[...pratos]
                .sort((a, b) => b.avaliacoes - a.avaliacoes)
                .slice(0, 10)}
              favoritos={favoritos}
              alternarFavorito={alternarFavorito}
            />

            <CategorySection
              title="Novidades"
              description="Descubra os novos pratos que chegaram."
              pratos={pratos.slice(-10)}
              favoritos={favoritos}
              alternarFavorito={alternarFavorito}
            />
          </>
        )}
      </section>
    </div>
  );
};

export default Home;
