import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "../components/Perfil/Perfil.css";
import { buscarPerfil } from "../services/Perfil.js";

// pegar as iniciais do nome do usuário, para mostrar no avatar
const gerarIniciais = (nome = "") =>
  nome
    .trim()
    .split(/\s+/)
    .slice(0, 2)
    .map((parte) => parte[0]?.toUpperCase() ?? "")
    .join("");

// icones em svg pq ficaram mais bonitinhos do q eu importei
const ICONES = {
  sino: [
    "M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9",
    "M10.3 21a1.94 1.94 0 0 0 3.4 0",
  ],
  talher: [
    "M3 2v7c0 1.1.9 2 2 2h4a2 2 0 0 0 2-2V2",
    "M7 2v20",
    "M21 15V2a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h3Zm0 0v7",
  ],
  cadeado: [
    "M5 11h14a2 2 0 0 1 2 2v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2Z",
    "M7 11V7a5 5 0 0 1 10 0v4",
  ],
  usuario: [
    "M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2",
    "M12 3a4 4 0 1 0 0 8 4 4 0 0 0 0-8Z",
  ],
  documento: [
    "M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z",
    "M14 2v6h6",
    "M16 13H8",
    "M16 17H8",
    "M10 9H8",
  ],
  coracao: [
    "M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z",
  ],
  mais: ["M5 12h14", "M12 5v14"],
  lapis: ["M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"],
  lixeira: [
    "M3 6h18",
    "M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6",
    "M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2",
  ],
  seta: ["m9 18 6-6-6-6"],
  folha: [
    "M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z",
    "M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12",
  ],
};

const Icone = ({ nome, tamanho = 22 }) => (
  <svg
    width={tamanho}
    height={tamanho}
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
    aria-hidden="true"
  >
    {ICONES[nome].map((d) => (
      <path key={d} d={d} />
    ))}
  </svg>
);

// linha de configuração (Alergias, Preferências, Senha, Conta)
const LinhaPerfil = ({ cor, icone, titulo, children, botao }) => (
  <section className={`perfil-linha perfil-linha-${cor}`}>
    <div className="perfil-linha-icone">
      <Icone nome={icone} tamanho={30} />
    </div>
    <div className="perfil-linha-texto">
      <h2>{titulo}</h2>
      {children}
    </div>
    {botao}
    <span className="perfil-linha-seta">
      <Icone nome="seta" tamanho={22} />
    </span>
  </section>
);

const Perfil = () => {
  const navigate = useNavigate();
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
      <header className="perfil-cabecalho">
        <div className="perfil-identidade">
          <div className="perfil-avatar-wrap">
            <div className="perfil-avatar" aria-hidden="true">
              {gerarIniciais(perfil.username)}
            </div>
            <span className="perfil-avatar-folha" aria-hidden="true">
              <Icone nome="folha" tamanho={16} />
            </span>
          </div>
          <div>
            <h1 className="perfil-nome">{perfil.username}</h1>
          </div>
        </div>

        <div className="perfil-stats">
          <div className="perfil-stat">
            <span className="perfil-stat-icone perfil-stat-verde">
              <Icone nome="documento" tamanho={24} />
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
              <Icone nome="coracao" tamanho={24} />
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

      <div className="perfil-conteudo">
        <LinhaPerfil
          cor="verde"
          icone="sino"
          titulo="Alergias"
          botao={
            <button
              type="button"
              className="perfil-botao perfil-botao-verde"
              onClick={() => navigate("/onboarding")}
            >
              <Icone
                nome={alergias.length > 0 ? "lapis" : "mais"}
                tamanho={18}
              />
              {alergias.length > 0 ? "Mudar alergias" : "Adicionar alergias"}
            </button>
          }
        >
          {alergias.length > 0 ? (
            <ul className="perfil-tags">
              {alergias.map((item) => (
                <li key={item} className="tag tag-alergia">
                  {item}
                </li>
              ))}
            </ul>
          ) : (
            <p className="perfil-descricao">Nenhuma alergia cadastrada.</p>
          )}
        </LinhaPerfil>

        <LinhaPerfil
          cor="amarelo"
          icone="talher"
          titulo="Preferências alimentares"
          botao={
            <button
              type="button"
              className="perfil-botao perfil-botao-amarelo"
              onClick={() => navigate("/onboarding")}
            >
              <Icone
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
            <ul className="perfil-tags">
              {preferencias.map((item) => (
                <li key={item} className="tag tag-preferencia">
                  {item}
                </li>
              ))}
            </ul>
          ) : (
            <p className="perfil-descricao">Nenhuma preferência cadastrada.</p>
          )}
        </LinhaPerfil>

        <LinhaPerfil
          cor="azul"
          icone="cadeado"
          titulo="Senha"
          botao={
            <button
              type="button"
              className="perfil-botao perfil-botao-contorno"
            >
              <Icone nome="lapis" tamanho={18} />
              Alterar senha
            </button>
          }
        >
          <p className="perfil-descricao">Mantenha sua conta segura.</p>
        </LinhaPerfil>

        <LinhaPerfil
          cor="vermelho"
          icone="usuario"
          titulo="Conta"
          botao={
            <button type="button" className="perfil-botao perfil-botao-perigo">
              <Icone nome="lixeira" tamanho={18} />
              Deletar conta
            </button>
          }
        >
          <p className="perfil-descricao">
            Gerencie as configurações da sua conta.
          </p>
        </LinhaPerfil>
      </div>
    </div>
  );
};

export default Perfil;
