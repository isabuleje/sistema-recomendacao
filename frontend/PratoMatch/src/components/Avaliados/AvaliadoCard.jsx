import styles from "./AvaliadoCard.module.css";
import { Heart } from "lucide-react";

const AvaliadoCard = ({
  titulo,
  descricao,
  imagem,
  categorias = [],
  tempo,
  nota,
  onOpenDetalhes,
  isFavorite,
  onToggleFavorite,
}) => {
  return (
    <div
      className={styles.cardContainer}
      role="button"
      tabIndex={0}
      onClick={onOpenDetalhes}
      onKeyDown={(event) => {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          onOpenDetalhes();
        }
      }}
    >
      {/* Lado Esquerdo: Imagem e Badges */}
      <div className={styles.cardImageWrapper}>
        <img src={imagem} alt={titulo} className={styles.cardImage} />

        <button
          className={`${styles.favoriteButton} ${isFavorite ? styles.favoriteButtonActive : ""}`}
          type="button"
          aria-label={
            isFavorite
              ? `Remover ${titulo} dos favoritos`
              : `Adicionar ${titulo} aos favoritos`
          }
          aria-pressed={isFavorite}
          onPointerDown={(event) => event.stopPropagation()}
          onClick={(event) => {
            event.stopPropagation();
            onToggleFavorite?.();
          }}
        >
          <Heart
            fill={isFavorite ? "currentColor" : "none"}
            aria-hidden="true"
          />
        </button>
      </div>

      {/* Centro: Informações da Pizza */}
      <div className={styles.cardContent}>
        <h3 className={styles.cardTitle}>{titulo}</h3>

        <div className={styles.cardMeta}>
          <span className={styles.metaItem}>
            <svg
              width="14"
              height="14"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <path d="M3 2v7c0 1.1.9 2 2 2h4a2 2 0 0 0 2-2V2"></path>
              <path d="M7 2v20"></path>
              <path d="M21 15V2v0a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h3Zm0 0v7"></path>
            </svg>
            {categorias[0] || "Sem categoria"}
          </span>
          <span className={styles.metaDot}>•</span>
          <span className={styles.metaItem}>
            <svg
              width="14"
              height="14"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <circle cx="12" cy="12" r="10"></circle>
              <polyline points="12 6 12 12 16 14"></polyline>
            </svg>
            {tempo} min
          </span>
        </div>

        <p className={styles.cardDescription}>{descricao}</p>

        {categorias.length > 0 && (
          <div className={styles.cardTags}>
            {categorias.slice(0, 3).map((categoria) => (
              <span
                key={categoria}
                className={`${styles.tag} ${styles.tagGreen}`}
              >
                {categoria}
              </span>
            ))}
          </div>
        )}
      </div>

      {/* Lado Direito: Avaliações e Botão */}
      <div className={styles.cardActions}>
        <div className={styles.cardStats}>
          <div className={styles.rating}>
            <svg
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="#FFAB00"
              stroke="#FFAB00"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
            </svg>
            <span className={styles.ratingScore}>Sua nota: {nota}</span>
          </div>
        </div>

        <button
          className={styles.btnDetalhes}
          type="button"
          onClick={(event) => {
            event.stopPropagation();
            onOpenDetalhes();
          }}
        >
          Ver detalhes
          <svg
            width="16"
            height="16"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <line x1="5" y1="12" x2="19" y2="12"></line>
            <polyline points="12 5 19 12 12 19"></polyline>
          </svg>
        </button>
      </div>
    </div>
  );
};

export default AvaliadoCard;
