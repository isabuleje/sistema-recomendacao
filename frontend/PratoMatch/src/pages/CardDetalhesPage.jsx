import { useLocation, useNavigate } from "react-router-dom";
import CardDetalhes from "../components/CardDetalhes.jsx";
import { useAvaliacao } from "../hooks/useAvaliacao.jsx";
import { imagemAleatoria } from "../utils/imagensPratos.js";

const CardDetalhesPage = () => {
  const { state } = useLocation();
  const navigate = useNavigate();
  const prato = state?.prato;
  const avaliacao = useAvaliacao(prato?.id, prato?.nota_usuario);

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
        imagem={  imagemAleatoria()}
        categorias={(prato.tags || []).join(", ") || "Sem categoria"}
        tempo={`${prato.tempo_preparo || 0} min`}
        calorias={prato.calorias || "Não informado"}
        numero_passos={prato.numero_passos || "Não informado"}
        passos={prato.passos || "Não informado"}
        ingredientes={(prato.ingredientes || []).join(", ") || "Não informado"}
        avaliacoes={prato.avaliacoes || 0}
        estrelas={prato.estrelas || 0}
        avaliacaoUsuario={avaliacao.nota}
        onAvaliar={avaliacao.avaliar}
      />
      {avaliacao.salvando && <p>Salvando avaliação...</p>}
      {avaliacao.erro && <p role="alert">{avaliacao.erro}</p>}
    </main>
  );
};

export default CardDetalhesPage;
