import { useEffect, useState } from "react";
import { NavLink, useNavigate } from "react-router-dom";
import styles from "../components/Avaliados/AvaliadoCard.module.css";
import AvaliadoCard from "../components/Avaliados/AvaliadoCard.jsx";
import { buscarPratosAvaliados } from "../services/Pratos.js";

const Avaliado = () => {
  const navigate = useNavigate();
  const [avaliados, setAvaliados] = useState([]);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState("");

  useEffect(() => {
    buscarPratosAvaliados()
      .then(setAvaliados)
      .catch(() => setErro("Não foi possível carregar seus pratos avaliados."))
      .finally(() => setCarregando(false));
  }, []);

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
          to="/avaliados"
          className={({ isActive }) =>
            `${styles["page-toggle-button"]} ${isActive ? styles["page-toggle-button-active"] : ""}`
          }
        >
          Avaliados
        </NavLink>
      </div>

      {carregando ? (
        <p>Carregando avaliações...</p>
      ) : erro ? (
        <p>{erro}</p>
      ) : avaliados.length === 0 ? (
        <p>Nenhum prato foi avaliado ainda.</p>
      ) : (
        avaliados.map((prato) => (
          <AvaliadoCard
            key={prato.id}
            titulo={prato.nome}
            descricao={prato.descricao || "Sem descrição disponível."}
            imagem={prato.imagem || "/Pratos/pizzar.jpg"}
            categorias={prato.tags || []}
            tempo={prato.tempo_preparo}
            nota={prato.nota_usuario}
            numerosNota={prato.avaliacoes}
            onOpenDetalhes={() =>
              navigate(`/pratos/${prato.id}`, { state: { prato } })
            }
          />
        ))
      )}
    </div>
  );
};

export default Avaliado;
