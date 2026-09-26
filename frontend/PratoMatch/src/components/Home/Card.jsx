import "./Cards.css";
import { Heart } from "lucide-react";

const Card = ({
  image,
  title,
  description,
  category,
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
        <div className="card-metadata">
          <span>{category}</span>
          <span>{prepTime} min </span>
          <span className="card-rating">⭐ {rating}</span>
        </div>
        <p className="card-description">{description}</p>
      </div>
    </div>
  );
};

export default Card;
