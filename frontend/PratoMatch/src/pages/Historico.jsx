// Página do Histórico, onde o usuário vê os pratos que favoritou
import { useEffect, useState } from "react";
import { NavLink, useNavigate } from "react-router-dom";
import styles from "../components/Historico/Card.module.css";
import Card from "../components/Historico/Card.jsx";
import { buscarPratoFavoritados, salvarFavoritos } from "../services/Pratos.js";
import { buscarPerfil } from "../services/Perfil.js";

// aceita tanto [ ... ] quanto { pratos: [ ... ] }
const extrairLista = (dados) =>
  Array.isArray(dados) ? dados : (dados?.pratos ?? []);

const classeAba = ({ isActive }) =>
  `${styles["page-toggle-button"]} ${
    isActive ? styles["page-toggle-button-active"] : ""
  }`;

const Historico = () => {
  const navigate = useNavigate();
  const [favoritos, setFavoritos] = useState([]);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState("");

  const [perfil, setPerfil] = useState(null);

  useEffect(() => {
    buscarPerfil()
      .then(setPerfil)
      .catch(() => setErro("Não foi possível carregar seu perfil."));
  }, []);

  useEffect(() => {
    buscarPratoFavoritados()
      .then((dados) => setFavoritos(extrairLista(dados)))
      .catch(() => setErro("Não foi possível carregar seus favoritos."))
      .finally(() => setCarregando(false));
  }, []);

  // ao desfavoritar, o prato sai da lista; se a API falhar, volta
  const desfavoritar = async (prato) => {
    setFavoritos((atuais) => atuais.filter((p) => p.id !== prato.id));

    try {
      await salvarFavoritos(prato.id, false);
    } catch (error) {
      setFavoritos((atuais) => [...atuais, prato]);
      console.error("Erro ao atualizar favorito:", error);
    }
  };

  return (
    <div className="home-page">
      <div className="user-greeting">
        <p style={{ color: "#055746", fontWeight: "700" }}>
          Olá, {perfil?.username ?? "usuário"}! 👋
        </p>
        <i className="bx bx-user" style={{ color: "#000504" }} />
      </div>

      <div
        className={styles["page-toggle"]}
        aria-label="Alternar entre histórico e avaliados"
      >
        <NavLink to="/historico" className={classeAba}>
          Favoritos
        </NavLink>
        <NavLink to="/avaliados" className={classeAba}>
          Avaliados
        </NavLink>
      </div>

      {carregando ? (
        <p>Carregando histórico...</p>
      ) : erro ? (
        <p>{erro}</p>
      ) : favoritos.length === 0 ? (
        <p>Você ainda não favoritou nenhum prato.</p>
      ) : (
        favoritos.map((prato) => (
          <Card
            key={prato.id}
            titulo={prato.nome}
            descricao={prato.descricao || "Sem descrição disponível."}
            imagem={prato.imagem || "/Pratos/pizzar.jpg"}
            categorias={prato.tags || []}
            tempo={prato.tempo_preparo}
            nota={prato.nota_usuario ?? 0}
            numerosNota={prato.avaliacoes}
            isFavorite
            onToggleFavorite={() => desfavoritar(prato)}
            onOpenDetalhes={() =>
              navigate(`/pratos/${prato.id}`, { state: { prato } })
            }
          />
        ))
      )}
    </div>
  );
};

export default Historico;
