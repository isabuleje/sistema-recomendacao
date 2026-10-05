import IconePerfil from "./IconePerfil.jsx";

import { gerarIniciais } from "../../utils/perfil.js";

function PerfilCabecalho({ perfil }) {
  return (
    <header className="perfil-cabecalho">
      <div className="perfil-identidade">
        <div className="perfil-avatar-wrap">
          <div className="perfil-avatar" aria-hidden="true">
            {gerarIniciais(perfil.username)}
          </div>

          <span className="perfil-avatar-folha" aria-hidden="true">
            <IconePerfil nome="folha" tamanho={16} />
          </span>
        </div>

        <div>
          <h1 className="perfil-nome">{perfil.username}</h1>
        </div>
      </div>

      <div className="perfil-stats">
        <div className="perfil-stat">
          <span className="perfil-stat-icone perfil-stat-verde">
            <IconePerfil nome="documento" tamanho={24} />
          </span>

          <div className="perfil-stat-texto">
            <span className="perfil-stat-numero">
              {perfil.pratos_avaliados ?? 0}
            </span>

            <span className="perfil-stat-legenda">Pratos avaliados</span>
          </div>
        </div>

        <div className="perfil-stat">
          <span className="perfil-stat-icone perfil-stat-amarelo">
            <IconePerfil nome="coracao" tamanho={24} />
          </span>

          <div className="perfil-stat-texto">
            <span className="perfil-stat-numero">
              {perfil.pratos_favoritados ?? 0}
            </span>

            <span className="perfil-stat-legenda">Pratos favoritos</span>
          </div>
        </div>
      </div>
    </header>
  );
}

export default PerfilCabecalho;
