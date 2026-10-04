import "./Cards.css";
import { Heart } from "lucide-react";

const Card = ({
  image,
  title,
  description,
  category,
  categories = [],
  prepTime,
  rating,
  isFavorite,
  onToggleFavorite,
  onOpenDetalhes,
}) => {
  return (
    <div
      className="card"
      role="button"
      tabIndex={0}
      aria-label={`Abrir detalhes de ${title}`}
      onClick={() => onOpenDetalhes?.()}
      onKeyDown={(event) => {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          onOpenDetalhes?.();
        }
      }}
    >
      <div className="card-image-wrapper">
        <img src={image} alt={title} className="card-image" />
        <button
          className={`favorite-button${isFavorite ? " is-favorite" : ""}`}
          type="button"
          aria-label={
            isFavorite
              ? `Remover ${title} dos favoritos`
              : `Adicionar ${title} aos favoritos`
          }
          aria-pressed={isFavorite}
          onPointerDown={(event) => event.stopPropagation()}
          onClick={(event) => {
            event.stopPropagation();
            onToggleFavorite();
          }}
        >
          <Heart
            fill={isFavorite ? "currentColor" : "none"}
            aria-hidden="true"
          />
        </button>
      </div>
      <div className="card-info">
        <h2 className="card-title">{title}</h2>
        <div className="card-metadata-row">

          <div className="card-metadata">
            <span className="metaItem">
              <svg
                width="14"
                height="14"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
                aria-hidden="true"
              >
                <circle cx="12" cy="12" r="10"></circle>
                <polyline points="12 6 12 12 16 14"></polyline>
              </svg>
              {prepTime} min
            </span>
            <span className="meta-dot" aria-hidden="true">
              •
            </span>
            <span className="card-rating">⭐ {rating}</span>
          </div>
        </div>
        <p className="card-description">{description}</p>

        {categories.length > 0 && (
          <ul className="card-tags" aria-label="Categorias do prato">
            {categories.slice(0, 2).map((item) => (
              <li key={item} className="card-tag">
                {item}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
};

export default Card;
