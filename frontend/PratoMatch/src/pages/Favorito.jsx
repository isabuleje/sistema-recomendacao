//Página do Histórico, onde o usuário vai poder ver os pratos que ele já avaliou e as avaliações que ele deu para cada prato
import { NavLink } from "react-router-dom";
import styles from "../components/Favorito/FavoritoCard.module.css";
import FavoritoCard from "../components/Favorito/FavoritoCard.jsx";

const Historico = () => {
  return (
    <div className="home-page">
      <div className="user-greeting">
        <p style={{ color: "#055746", fontWeight: "700" }}> Olá, usuário! 👋</p>
        <i className="bx bx-user" style={{ color: "#000504" }} />
      </div>

      <div
        className={styles["page-toggle"]}
        aria-label="Alternar entre histórico e favoritos"
      >
        <NavLink
          to="/historico"
          className={({ isActive }) =>
            `${styles["page-toggle-button"]} ${isActive ? styles["page-toggle-button-active"] : ""}`
          }
        >
          Histórico
        </NavLink>
        <NavLink
          to="/favoritos"
          className={({ isActive }) =>
            `${styles["page-toggle-button"]} ${isActive ? styles["page-toggle-button-active"] : ""}`
          }
        >
          Favoritos
        </NavLink>
      </div>

      <FavoritoCard
        titulo="Pizza Margherita"
        descricao="Massa artesanal, molho de tomate, mussarela de búfala e manjericão fresco."
        imagem="https://images.unsplash.com/photo-1574071318508-1cdbab80d002?auto=format&fit=crop&q=80&w=400"
        tempo="25 min"
        nota="4,8"
        numerosNota="(1,2k)"
      />

      <FavoritoCard
        titulo="Pizza Margherita"
        descricao="Massa artesanal, molho de tomate, mussarela de búfala e manjericão fresco."
        imagem="https://images.unsplash.com/photo-1574071318508-1cdbab80d002?auto=format&fit=crop&q=80&w=400"
        tempo="25 min"
        nota="4,8"
        numerosNota="(1,2k)"
      />

      <FavoritoCard
        titulo="Pizza Margherita"
        descricao="Massa artesanal, molho de tomate, mussarela de búfala e manjericão fresco."
        imagem="https://images.unsplash.com/photo-1574071318508-1cdbab80d002?auto=format&fit=crop&q=80&w=400"
        tempo="25 min"
        nota="4,8"
        numerosNota="(1,2k)"
        data="21 de setembro de 2025"
      />

      <FavoritoCard
        titulo="Pizza Margherita"
        descricao="Massa artesanal, molho de tomate, mussarela de búfala e manjericão fresco."
        imagem="https://images.unsplash.com/photo-1574071318508-1cdbab80d002?auto=format&fit=crop&q=80&w=400"
        tempo="25 min"
        nota="4,8"
        numerosNota="(1,2k)"
        data="21 de setembro de 2025"
      />
    </div>
  );
};

export default Historico;
