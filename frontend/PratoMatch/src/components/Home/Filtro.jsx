import { useEffect, useState } from "react";
import { buscarIngredientes } from "../../services/pratosService.js";
import "./Filtro.css";

const FilterSection = ({ ingredientes = [], onAdicionar, onRemover }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [opcoes, setOpcoes] = useState([]);
  const [buscaIngrediente, setBuscaIngrediente] = useState("");

  useEffect(() => {
    buscarIngredientes()
      .then(setOpcoes)
      .catch((erro) => console.error("Erro ao buscar ingredientes:", erro));
  }, []);

  const opcoesVisiveis = opcoes
    .filter((ingrediente) =>
      ingrediente.toLocaleLowerCase().includes(
        buscaIngrediente.trim().toLocaleLowerCase(),
      ),
    )
    .slice(0, 20);

  const selecionarIngrediente = (ingrediente) => {
    onAdicionar?.(ingrediente);
    setBuscaIngrediente("");
  };

  return (
    <section className="filter-section">
      <button
        className="filter-button"
        type="button"
        onClick={() => setIsOpen(!isOpen)}
      >
        <i className="bx bx-filter" aria-hidden="true" />
        Filtros
      </button>

      {isOpen && (
        <div className="filter-options">
          <input
            type="text"
            className="ingredient-search"
            value={buscaIngrediente}
            onChange={(event) => setBuscaIngrediente(event.target.value)}
            placeholder="Buscar ingrediente"
            aria-label="Buscar ingrediente"
          />

          <div className="ingredient-options">
            {opcoesVisiveis.map((ingrediente) => (
              <button
                type="button"
                className="ingredient-option"
                key={ingrediente}
                onClick={() => selecionarIngrediente(ingrediente)}
              >
                {ingrediente}
              </button>
            ))}
          </div>

          {ingredientes.length > 0 && (
            <div className="selected-ingredients">
              {ingredientes.map((ingrediente) => (
                <button
                  type="button"
                  className="selected-ingredient"
                  key={ingrediente}
                  onClick={() => onRemover?.(ingrediente)}
                  aria-label={`Remover ingrediente ${ingrediente}`}
                >
                  {ingrediente} ×
                </button>
              ))}
            </div>
          )}
        </div>
      )}
    </section>
  );
};

export default FilterSection;
