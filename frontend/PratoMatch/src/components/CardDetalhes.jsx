//Deixar fora da pasta pq acho q vou utilizar no Home, Historico e Favoritos tudo a mesma coisa
import "./CardDetalhes.css";

//dps n posso esquecer q esse e o lugar q vai ter as estrelas
const CardDetalhes = ({
  titulo,
  descricao,
  imagem,
  categorias,
  tempo,
  calorias,
  numero_passos,
  passos,
  nutricao,
  ingredientes,
  avaliações,
  estrelas,
}) => {
  return (
    <div className="card-detalhes">
      <div className="card-detalhes-imagem">
        <img src={imagem} alt={titulo} />
      </div>

      <div className="card-detalhes-conteudo">
        <h2 className="card-detalhes-titulo">{titulo}</h2>
        <p className="card-detalhes-descricao">{descricao}</p>
        <p className="card-detalhes-categorias">{categorias}</p>
        <p className="card-detalhes-tempo">{tempo}</p>
        <p className="card-detalhes-calorias">"Calorias: "{calorias}</p>
        <p className="card-detalhes-numero-passos">"Número de passos: "{numero_passos}</p>
        <p className="card-detalhes-passos">"Passos: "{passos}</p>
        <p className="card-detalhes-nutricao">"Nutrição: "{nutricao}</p>
        <p className="card-detalhes-ingredientes">{ingredientes}</p>
        <p className="card-detalhes-avaliacoes">"Quantidade de avaliações: "{avaliações}</p>
        <p className="card-detalhes-estrelas">{estrelas}</p>
      </div>
    </div>
  );
};

export default CardDetalhes;
