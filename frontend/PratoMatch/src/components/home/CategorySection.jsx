import CardGrid from "./CardGrid.jsx";
/*
  O CategorySection exibe uma seção de pratos
  A ideia original era ter 3 seções (recomendados, populares e novidadees)
  Mas como teve mil um problemas no só nas recomendações da seção recomendados, melhor nem ter o resto

  Em resumo aq organiza o título, descrição e a lista de pratos (CardGrid) e passa as props pra ele
 */
function CategorySection({
  title,
  description,
  pratos,
  paginaAtual,
  totalPaginas,
  onMudarPagina,
  favoritos,
  onToggleFavorite,
}) {
  return (
    <section className="category-section">
      <div className="category-heading">
        <h2 className="category-title">{title}</h2>

        <p className="category-description">{description}</p>
      </div>

      <CardGrid
        pratos={pratos}
        paginaAtual={paginaAtual}
        totalPaginas={totalPaginas}
        onMudarPagina={onMudarPagina}
        favoritos={favoritos}
        onToggleFavorite={onToggleFavorite}
      />
    </section>
  );
}

export default CategorySection;
