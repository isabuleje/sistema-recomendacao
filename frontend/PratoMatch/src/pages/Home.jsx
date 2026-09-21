// Página inicial, onde o usuário vai poder ver os pratos recomendados, pratos populares e novidades
import ShadowText from "../components/ShadowText/ShadowText";
import "../components/Home/Placa.css";
import { Search, Send } from "lucide-react";
import Card from "../components/Home/Card";
import FilterSection from "../components/Home/Filtro.jsx";
import { useRef } from "react";

const CategorySection = ({ title, description }) => (
  <section className="category-section">
    <h2 className="category-title" style={{ color: "#055746" }}>
      {title}
    </h2>
    <p  style={{ fontSize: '16px' }}> 
      {description}
    </p>
    <CardRail title={title} />

  </section>
);

const CardRail = ({ title }) => {
  const cardsRef = useRef(null);
  const dragState = useRef({ isDragging: false, startX: 0, startScrollLeft: 0 });

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
      {[1, 2, 3, 4,5,6,7,8].map((number) => (
        <Card
          key={`${title}-${number}`}
          title={`Prato ${number}`}
          description={`Descrição do prato ${number}`}
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
      <div className="placa">
            <h2 className="placa-texto" style={{ color: "#055746" }}>
              Encontre o prato perfeito para o momento perfeito!
            </h2>
          <p>
            Receitas personalizadas com base no seu perfil, preferências e avaliações.
          </p>
      </div>

      <section className="home-content">
        <div className="input-wrapper">
          <Search className="search-icon" />
          <input
            type="text"
            placeholder="O que você quer comer hoje?"
            name="text"
            className="input"
          />
          <button className="send-button" type="button" aria-label="Pesquisar">
            <Send />
          </button>
        </div>

        <FilterSection />

        <CategorySection title="Recomendados para você" description="Encontre os pratos mais indicados para o seu gosto." />
        <CategorySection title="Pratos populares" description="Os pratos mais pedidos pelos nossos usuários." />
        <CategorySection title="Novidades" description="Descubra os novos pratos que chegaram." />
      </section>
    </div>
  );
};

export default Home;