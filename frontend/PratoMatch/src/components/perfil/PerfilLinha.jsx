import IconePerfil from "./IconePerfil.jsx";

function PerfilLinha({ cor, icone, titulo, children, botao }) {
  return (
    <section className={`perfil-linha perfil-linha-${cor}`}>
      <div className="perfil-linha-icone">
        <IconePerfil nome={icone} tamanho={30} />
      </div>

      <div className="perfil-linha-texto">
        <h2>{titulo}</h2>

        {children}
      </div>

      {botao}

      <span className="perfil-linha-seta">
        <IconePerfil nome="seta" tamanho={22} />
      </span>
    </section>
  );
}

export default PerfilLinha;
