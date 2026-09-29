import { useEffect, useState } from "react";
import "../components/Perfil/Perfil.css";
import { buscarPerfil } from "../services/Perfil.js";

// pegar as inciais do nome do usuário, para mostrar no avatar
const gerarIniciais = (nome = "") =>
  nome
    .trim()
    .split(/\s+/)
    .slice(0, 2)
    .map((parte) => parte[0]?.toUpperCase() ?? "")
    .join("");

const Perfil = () => {
  const [perfil, setPerfil] = useState(null);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState("");

  useEffect(() => {
    buscarPerfil()
      .then(setPerfil)
      .catch(() => setErro("Não foi possível carregar seu perfil."))
      .finally(() => setCarregando(false));
  }, []);

  if (carregando) return <p>Carregando perfil...</p>;
  if (erro) return <p>{erro}</p>;
  if (!perfil) return null;

  const alergias = perfil.alergias ?? [];
  const preferencias = perfil.preferencias ?? [];

  return (
    <div className="perfil-page">
      {/*Coluna esquerda: avatar, nome, alergias e preferências*/}
      <div className="perfil-esquerda">
        <div className="perfil-identidade">
          <div className="perfil-avatar" aria-hidden="true">
            {gerarIniciais(perfil.username)}
          </div>
          <h1 className="perfil-nome">{perfil.username}</h1>
        </div>

        <div className="perfil-coluna-alergia-preferencia">
          {/*-------------- ALERGIAS --------------*/}
          <div className="perfil-alergias">
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
          </div>

          {/*-------------- PREFERÊNCIAS --------------*/}
          <div className="perfil-preferencias">
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
          </div>

        </div>
      </div>

      {/*Coluna direita: estatísticas e ações*/}
      <div className="perfil-coluna-direita">
        <div className="perfil-stats">
          <div className="perfil-stat">
            <span className="perfil-stat-numero">
              {perfil.pratos_avaliados ?? 0}
            </span>
            <span className="perfil-stat-legenda">Pratos avaliados</span>
          </div>

          <div className="perfil-stat">
            <span className="perfil-stat-numero">
              {perfil.pratos_favoritados ?? 0}
            </span>
            <span className="perfil-stat-legenda">Pratos favoritados</span>
          </div>
        </div>

        <div className="perfil-acoes">
          <button type="button" className="perfil-botao">
            Mudar alergias
          </button>
          <button type="button" className="perfil-botao">
            Mudar preferências
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
