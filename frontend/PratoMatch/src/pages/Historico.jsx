//Página do Histórico, onde o usuário vai poder ver os pratos que ele já avaliou e as avaliações que ele deu para cada prato
import { NavLink } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import styles from "../components/Historico/Card.module.css";
import Card from "../components/Historico/Card.jsx";

const historicoPratos = Array.from({ length: 6 }, (_, indice) => ({
  id: `historico-${indice + 1}`,
  titulo: "Pizza Margherita",
  descricao:
    "Massa artesanal, molho de tomate, mussarela de búfala e manjericão fresco.",
  imagem:
    "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?auto=format&fit=crop&q=80&w=400",
  tempo: "25 min",
  nota: "4,8",
  numerosNota: "(1,2k)",
  data: "21 de setembro de 2025",
}));

const Historico = ({ favoritos = [], alternarFavorito = () => {} }) => {
  const navigate = useNavigate();

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

      {historicoPratos.map((prato) => (
        <Card
          key={prato.id}
          {...prato}
          isFavorite={favoritos.some((favorito) => favorito.id === prato.id)}
          onToggleFavorite={alternarFavorito}
          onOpenDetalhes={() =>
            navigate(`/pratos/${prato.id}`, { state: { prato } })
          }
        />
      ))}
    </div>
  );
};

export default Historico;
