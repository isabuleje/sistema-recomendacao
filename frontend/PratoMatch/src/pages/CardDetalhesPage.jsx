import { useLocation, useNavigate } from "react-router-dom";
import CardDetalhes from "../components/CardDetalhes.jsx";

const CardDetalhesPage = () => {
  const { state } = useLocation();
  const navigate = useNavigate();
  const prato = state?.prato;

  if (!prato) {
    return (
      <main className="home-page">
        <p>Não foi possível carregar os detalhes deste prato.</p>
        <button type="button" onClick={() => navigate(-1)}>
          Voltar
        </button>
      </main>
    );
  }

  return (
    <main className="card-detalhes-pagina">
      <button
        type="button"
        className="card-detalhes-voltar"
        onClick={() => navigate(-1)}
      >
        ← Voltar
      </button>
      <CardDetalhes
        titulo={prato.nome}
        descricao={prato.descricao || "Sem descrição disponível."}
        imagem={prato.imagem || "/Pratos/prato1.webp"}
        categorias={(prato.tags || []).join(", ") || "Sem categoria"}
        tempo={`${prato.tempo_preparo || 0} min`}
        calorias={prato.calorias || "Não informado"}
        numero_passos={prato.numero_passos || "Não informado"}
        passos={prato.passos || "Não informado"}
        ingredientes={(prato.ingredientes || []).join(", ") || "Não informado"}
        avaliações={prato.avaliacoes || 0}
        estrelas={prato.estrelas || 0}
      />
    </main>
  );
};

export default CardDetalhesPage;
