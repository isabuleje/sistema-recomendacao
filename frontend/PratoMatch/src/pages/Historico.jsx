//Página do Histórico, onde o usuário vai poder ver os pratos que ele já avaliou e as avaliações que ele deu para cada prato
import { NavLink } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import styles from "../components/Historico/Card.module.css";
import Card from "../components/Historico/Card.jsx";
import { useState, useEffect } from "react";
import { buscarPratosAvaliados } from "../services/Pratos.js";


//Pra quando os favoritos estiverem funcionando, essa página vai dar pra ver os avaliados e favoritados
/*{favoritos.map((prato) => (
        <Card
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
      ))}
*/

const Historico = () => {
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
        <p>Carregando histórico...</p>
      ) : erro ? (
        <p>{erro}</p>
      ) : (
        <p>Nenhum prato avaliado encontrado.</p>
      )}

      
      {avaliados.map((prato) => (
        <Card
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
      ))}
    </div>
  );
};

export default Historico;
