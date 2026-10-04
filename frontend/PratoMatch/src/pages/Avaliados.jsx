import { NavLink, useNavigate } from "react-router-dom";

import styles from "../components/avaliados/AvaliadoCard.module.css";

import AvaliadoCard from "../components/avaliados/AvaliadoCard.jsx";

import { useAvaliacao } from "../hooks/useAvaliados.jsx";
import { useFavoritos } from "../hooks/useFavoritos.jsx";
import { usePerfil } from "../hooks/usePerfil.js";

import { imagemDoPrato } from "../utils/imagensPratos.js";

const Avaliado = () => {
  const navigate = useNavigate();

  const { avaliados, carregando, erro } = useAvaliacao();
  const { favoritos, alternarFavorito: alternarFavoritoPersistido } =
    useFavoritos();

  const { perfil } = usePerfil();

  const abrirDetalhes = (prato) => {
    navigate(`/pratos/${prato.id}`, {
      state: { prato },
    });
  };

  return (
    <div className="home-page">
      <div className="user-greeting">
        <p>Olá, {perfil?.username ?? "usuário"}! 👋</p>

        <i className="bx bx-user" aria-hidden="true" />
      </div>

      <div
        className={styles["page-toggle"]}
        aria-label="Alternar entre histórico e favoritos"
      >
        <NavLink
          to="/historico"
          className={({ isActive }) =>
            `${styles["page-toggle-button"]} ${
              isActive ? styles["page-toggle-button-active"] : ""
            }`
          }
        >
          Favoritos
        </NavLink>

        <NavLink
          to="/avaliados"
          className={({ isActive }) =>
            `${styles["page-toggle-button"]} ${
              isActive ? styles["page-toggle-button-active"] : ""
            }`
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
            imagem={imagemDoPrato(prato.id)}
            categorias={prato.tags || []}
            tempo={prato.tempo_preparo}
            nota={prato.nota_usuario}
            numerosNota={prato.avaliacoes}
            isFavorite={favoritos.has(Number(prato.id))}
            onToggleFavorite={() => alternarFavoritoPersistido(prato.id)}
            onOpenDetalhes={() => abrirDetalhes(prato)}
          />
        ))
      )}
    </div>
  );
};

export default Avaliado;
