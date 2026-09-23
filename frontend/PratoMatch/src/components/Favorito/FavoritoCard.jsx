import styles from "./FavoritoCard.module.css";

const FavoritoCard = ({
  titulo,
  descricao,
  imagem,
  tempo,
  nota,
  numerosNota,
}) => {
  return (
    <div className={styles.cardContainer}>
      {/* Lado Esquerdo: Imagem e Badges */}
      <div className={styles.cardImageWrapper}>
        <div className={styles.badgeHeart}>
          <svg
            width="20"
            height="20"
            viewBox="0 0 24 24"
            fill="#e53935"
            stroke="#e53935"
            strokeWidth="1.5"
          >
            <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78L12 21.23l8.84-8.84a5.5 5.5 0 0 0 0-7.78Z" />
          </svg>
        </div>
        <img src={imagem} alt={titulo} className={styles.cardImage} />
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
            Italiana
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
            {tempo}
          </span>
        </div>

        <p className={styles.cardDescription}>{descricao}</p>

        <div className={styles.cardTags}>
          <span className={`${styles.tag} ${styles.tagGreen}`}>
            Vegetariano
          </span>
          <span className={`${styles.tag} ${styles.tagGreen}`}>Sem Glúten</span>
          <span className={`${styles.tag} ${styles.tagOrange}`}>Italiano</span>
        </div>
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
            <span className={styles.ratingScore}>{nota}</span>
            <span className={styles.ratingCount}>{numerosNota}</span>
          </div>
        </div>

        <button className={styles.btnDetalhes}>
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

export default FavoritoCard;
