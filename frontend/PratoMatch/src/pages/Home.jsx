// Página inicial, onde o usuário vai poder ver os pratos recomendados, pratos populares e novidades
import "../components/Home/Placa.css";
import "../components/Home/Categorias.css";
import "../components/Home/Input.css";

import { Search, Send } from "lucide-react";
import Card from "../components/Home/Card";
import FilterSection from "../components/Home/Filtro.jsx";
import { useRef } from "react";

const CategorySection = ({ title, description }) => (
  <section className="category-section">
    <div className="category-heading">
      <h2 className="category-title" style={{ color: "#055746" }}>
        {title}
      </h2>
      <p>{description}</p>
    </div>
    <CardRail title={title} />
  </section>
);

const CardRail = ({ title }) => {
  const cardsRef = useRef(null);
  const dragState = useRef({
    isDragging: false,
    startX: 0,
    startScrollLeft: 0,
  });

  const handlePointerDown = (event) => {
    if (event.pointerType === "mouse" && event.button !== 0) return;

    dragState.current = {
      isDragging: true,
      startX: event.clientX,
      startScrollLeft: cardsRef.current.scrollLeft,
    };
    cardsRef.current.setPointerCapture(event.pointerId);
    cardsRef.current.classList.add("is-dragging");
  };

  const handlePointerMove = (event) => {
    if (!dragState.current.isDragging) return;

    const distance = event.clientX - dragState.current.startX;
    cardsRef.current.scrollLeft = dragState.current.startScrollLeft - distance;
  };

  const stopDragging = (event) => {
    if (!dragState.current.isDragging) return;

    dragState.current.isDragging = false;
    cardsRef.current.releasePointerCapture?.(event.pointerId);
    cardsRef.current.classList.remove("is-dragging");
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
        {[1, 2, 3, 4, 5, 6, 7, 8].map((number) => (
          <Card
            key={`${title}-${number}`}
            title={`Prato ${number}`}
            description={`Prato muito aura + ego, larper Tung tung Sahur, amongos, tralelelo tralala, 67 67 67 67`}
            category="Massas"
            prepTime="35 min"
            rating="4,8 ★"
            image="/Pratos/pizzar.jpg"
          />
        ))}
      </div>
    </div>
  );
};

const Home = () => {
  return (
    <div className="home-page">
      <div className="user-greeting">
        <p style={{ color: "#055746", fontWeight: "700" }}> Olá, usuário! 👋</p>
        <i class="bx bx-user" style={{ color: "#000504" }} />
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

        <CategorySection
          title="Recomendados para você"
          description="Encontre os pratos mais indicados para o seu gosto."
        />
        <CategorySection
          title="Pratos populares"
          description="Os pratos mais pedidos pelos nossos usuários."
        />
        <CategorySection
          title="Novidades"
          description="Descubra os novos pratos que chegaram."
        />
      </section>
    </div>
  );
};

export default Home;
