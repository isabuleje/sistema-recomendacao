import { useState } from "react";
import "./Filtro.css";

const FilterSection = () => {
  const [isOpen, setIsOpen] = useState(false);

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
          <label>
            <input type="checkbox" name="vegetariano" />
            Vegetariano
          </label>

          <label>
            <input type="checkbox" name="vegano" />
            Vegano
          </label>

          <label>
            <input type="checkbox" name="onivoro" />
            Onívoro
          </label>

          <label>
            <input type="checkbox" name="semGluten" />
            Sem Glúten
          </label>

          <label>
            <input type="checkbox" name="semLactose" />
            Sem Lactose
          </label>

          <label>
            <input type="checkbox" name="baixaCalorias" />
            Baixa Calorias
          </label>
        </div>
      )}
    </section>
  );
};

export default FilterSection;
