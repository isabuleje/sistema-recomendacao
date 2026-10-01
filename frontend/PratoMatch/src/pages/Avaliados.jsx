import { useEffect, useState } from "react";
import { NavLink, useNavigate } from "react-router-dom";
import styles from "../components/avaliados/AvaliadoCard.module.css";
import AvaliadoCard from "../components/avaliados/AvaliadoCard.jsx";
import { buscarPratosAvaliados, salvarFavoritos } from "../services/pratosService.js";
import { buscarPerfil } from "../services/perfilService.js";
import { imagemAleatoria } from "../utils/imagensPratos.js";

const Avaliado = () => {
  const navigate = useNavigate();
  const [avaliados, setAvaliados] = useState([]);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState("");

  useEffect(() => {
    buscarPratosAvaliados()
      .then((dados) =>
        setAvaliados(Array.isArray(dados) ? dados : (dados?.pratos ?? [])),
      )
      .catch(() => setErro("Não foi possível carregar seus pratos avaliados."))
      .finally(() => setCarregando(false));
  }, []);

  const [perfil, setPerfil] = useState(null);

  useEffect(() => {
    buscarPerfil()
      .then(setPerfil)
      .catch(() => setErro("Não foi possível carregar seu perfil."));
  }, []);

  const alternarFavorito = async (prato) => {
    const novo = !prato.is_favorito;

    // otimista: atualiza só esse prato na lista
    setAvaliados((atuais) =>
      atuais.map((p) => (p.id === prato.id ? { ...p, is_favorito: novo } : p)),
    );

    try {
      await salvarFavoritos(prato.id, novo);
    } catch (error) {
      // reverte se a API falhar
      setAvaliados((atuais) =>
        atuais.map((p) =>
          p.id === prato.id ? { ...p, is_favorito: !novo } : p,
        ),
      );
      console.error("Erro ao atualizar favorito:", error);
    }
  };

  return (
    <div className="home-page">
      <div className="user-greeting">
        <p style={{ color: "#055746", fontWeight: "700" }}>
          {" "}
          Olá, {perfil?.username ?? "usuário"}! 👋
        </p>
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
          Favoritos
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
            imagem={imagemAleatoria()}
            categorias={prato.tags || []}
            tempo={prato.tempo_preparo}
            nota={prato.nota_usuario}
            numerosNota={prato.avaliacoes}
            isFavorite={prato.is_favorito}
            onToggleFavorite={() => alternarFavorito(prato)}
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
