// Perfil onde o usuário vai poder ver suas informações, alterar suas informações
// e mudar se ele possui alergia ou é vegetariano, vegano ou onívoro
import "../components/Perfil/Perfil.css";

const Perfil = () => {
  // Dados de exemplo — troque pelos dados reais do usuário (state, context, API etc.)
  const usuario = {
    nome: "Marina Souza",
    iniciais: "MS",
    pratosAvaliados: 47,
    pratosFavoritados: 12,
  };

  const alergias = ["Amendoim", "Frutos do mar"];
  const preferencias = ["Vegetariano"];

  return (
    <div className="perfil-page">
      <div className="perfil-tudo-esquerda">
        <div className="perfil-coluna-esquerda">
          <div className="perfil-avatar" aria-hidden="true">
            {usuario.iniciais}
          </div>
          <h1 className="perfil-nome">{usuario.nome}</h1>
        </div>

        <div className="perfil-coluna-alergia-preferencia">
          <section className="perfil-secao">
            <h2>Alergias</h2>
            {alergias.length > 0 ? (
              <ul className="perfil-tags">
                {alergias.map((item) => (
                  <li key={item} className="tag tag-alergia">
                    {item}
                  </li>
                ))}
              </ul>
            ) : (
              <p className="perfil-vazio">Nenhuma alergia cadastrada.</p>
            )}
          </section>

          <section className="perfil-secao">
            <h2>Preferências alimentares</h2>
            {preferencias.length > 0 ? (
              <ul className="perfil-tags">
                {preferencias.map((item) => (
                  <li key={item} className="tag tag-preferencia">
                    {item}
                  </li>
                ))}
              </ul>
            ) : (
              <p className="perfil-vazio">Nenhuma preferência cadastrada.</p>
            )}
          </section>
        </div>
      </div>

      <div className="perfil-coluna-direita">
        <div className="perfil-stats">
          <div className="perfil-stat">
            <span className="perfil-stat-numero">
              {usuario.pratosAvaliados}
            </span>
            <span className="perfil-stat-legenda">Pratos avaliados</span>
          </div>

          <div className="perfil-stat">
            <span className="perfil-stat-numero">
              {usuario.pratosFavoritados}
            </span>
            <span className="perfil-stat-legenda">Pratos favoritados</span>
          </div>
        </div>

        <div className="perfil-acoes">
          <button type="button" className="perfil-botao">
            Mudar perfil
          </button>
          <button type="button" className="perfil-botao">
            Mudar preferências
          </button>
          <button type="button" className="perfil-botao">
            Mudar alergias
          </button>
          <button type="button" className="perfil-botao">
            Mudar senha
          </button>
          <button type="button" className="perfil-botao perfil-botao-perigo">
            Deletar conta
          </button>
        </div>
      </div>
    </div>
  );
};

export default Perfil;
