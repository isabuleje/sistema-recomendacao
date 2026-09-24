//Página do Histórico, onde o usuário vai poder ver os pratos que ele já avaliou e as avaliações que ele deu para cada prato
import { NavLink } from "react-router-dom";
import styles from "../components/Favorito/FavoritoCard.module.css";
import FavoritoCard from "../components/Favorito/FavoritoCard.jsx";

const Favorito = ({ favoritos = [], alternarFavorito = () => {} }) => {
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

      {favoritos.length === 0 ? (
        <p>Nenhum prato foi favoritado ainda.</p>
      ) : (
        favoritos.map((prato) => (
          <FavoritoCard
            key={prato.id}
            titulo={prato.nome}
            descricao={prato.descricao || "Sem descrição disponível."}
            imagem="/Pratos/pizzar.jpg"
            tempo={`${prato.tempo_preparo || "--"} min`}
            nota={prato.estrelas || "--"}
            numerosNota={prato.avaliacoes ? `(${prato.avaliacoes})` : ""}
            onToggleFavorite={() => alternarFavorito(prato)}
          />
        ))
      )}
    </div>
  );
};

export default Favorito;
