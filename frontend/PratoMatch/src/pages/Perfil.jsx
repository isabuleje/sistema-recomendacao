import { useNavigate } from "react-router-dom";

import "../components/Perfil/Perfil.css";

import IconePerfil from "../components/Perfil/IconePerfil.jsx";
import PerfilCabecalho from "../components/Perfil/PerfilCabecalho.jsx";
import PerfilLinha from "../components/Perfil/PerfilLinha.jsx";
import PerfilTags from "../components/Perfil/PerfilTags.jsx";

import { usePerfil } from "../hooks/usePerfil.js";

const Perfil = () => {
  const navigate = useNavigate();

  const { perfil, carregando, erro } = usePerfil();

  if (carregando) {
    return <p>Carregando perfil...</p>;
  }

  if (erro) {
    return <p>{erro}</p>;
  }

  if (!perfil) {
    return null;
  }

  const alergias = perfil.alergias ?? [];
  const preferencias = perfil.preferencias ?? [];

  return (
    <div className="perfil-page">
      <PerfilCabecalho perfil={perfil} />

      <div className="perfil-conteudo">
        {/* Alergias */}

        <PerfilLinha
          cor="verde"
          icone="sino"
          titulo="Alergias"
          botao={
            <button
              type="button"
              className="perfil-botao perfil-botao-verde"
              onClick={() => navigate("/onboarding")}
            >
              <IconePerfil
                nome={alergias.length > 0 ? "lapis" : "mais"}
                tamanho={18}
              />

              {alergias.length > 0 ? "Mudar alergias" : "Adicionar alergias"}
            </button>
          }
        >
          {alergias.length > 0 ? (
            <PerfilTags itens={alergias} tipo="alergia" />
          ) : (
            <p className="perfil-descricao">Nenhuma alergia cadastrada.</p>
          )}
        </PerfilLinha>

        {/* Preferências */}
        <PerfilLinha
          cor="amarelo"
          icone="talher"
          titulo="Preferências alimentares"
          botao={
            <button
              type="button"
              className="perfil-botao perfil-botao-amarelo"
              onClick={() => navigate("/onboarding")}
            >
              <IconePerfil
                nome={preferencias.length > 0 ? "lapis" : "mais"}
                tamanho={18}
              />

              {preferencias.length > 0
                ? "Mudar preferências"
                : "Adicionar preferências"}
            </button>
          }
        >
          {preferencias.length > 0 ? (
            <PerfilTags itens={preferencias} tipo="preferencia" />
          ) : (
            <p className="perfil-descricao">Nenhuma preferência cadastrada.</p>
          )}
        </PerfilLinha>

        {/* Senha */}

        <PerfilLinha
          cor="azul"
          icone="cadeado"
          titulo="Senha"
          botao={
            <button
              type="button"
              className="perfil-botao perfil-botao-contorno"
            >
              <IconePerfil nome="lapis" tamanho={18} />
              Alterar senha
            </button>
          }
        >
          <p className="perfil-descricao">Mantenha sua conta segura.</p>
        </PerfilLinha>

        {/* Conta */}
        <PerfilLinha
          cor="vermelho"
          icone="usuario"
          titulo="Conta"
          botao={
            <button type="button" className="perfil-botao perfil-botao-perigo">
              <IconePerfil nome="lixeira" tamanho={18} />
              Deletar conta
            </button>
          }
        >
          <p className="perfil-descricao">
            Gerencie as configurações da sua conta.
          </p>
        </PerfilLinha>
      </div>
    </div>
  );
};

export default Perfil;
