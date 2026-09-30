import {imagemAleatoria} from "../../utils/imagensPratos.js";

const CardPratoCirculo = ({ prato, selecionado, onToggle }) => (
  <button
    type="button"
    className={"prato-circulo" + (selecionado ? " prato-circulo-ativo" : "")}
    aria-pressed={selecionado}
    onClick={onToggle}
  >
    <span className="prato-circulo-imagem">
      <img src={imagemAleatoria()} alt="" />
      {selecionado && <span className="prato-circulo-check">✓</span>}
    </span>
    <span className="prato-circulo-nome">{prato.nome}</span>
  </button>
);

export default CardPratoCirculo;
