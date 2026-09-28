import { useState } from "react";
import { useNavigate } from "react-router-dom";

import styles from "../components/Cadastro/Cadastro.module.css";

function Cadastro() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [erro, setErro] = useState("");

  const [isRightPanelActive, setIsRightPanelActive] = useState(false);
  const navigate = useNavigate();

  const cadastrar = async (e) => {
    e.preventDefault();
    setErro("");
    try {
      const resposta = await fetch("http://127.0.0.1:8000/api/cadastro/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify({
          username,
          password,
        }),
      });

      const dados = await resposta.json();

      if (!resposta.ok) {
        throw new Error(dados.erro || "Erro no cadastro.");
      }

      console.log("Usuário criado:", dados);
      navigate("/OnBoarding");
    } catch (erro) {
      setErro(erro.message);
    }
  };

  const entrar = async (e) => {
    e.preventDefault();
    setErro("");

    try {
      const resposta = await fetch("http://127.0.0.1:8000/api/login/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify({ username, password }),
      });
      const dados = await resposta.json();

      if (!resposta.ok) {
        throw new Error(dados.erro || "Erro ao entrar.");
      }

      navigate("/home");
    } catch (error) {
      setErro(error.message);
    }
  };

  return (
    <div className={styles.cadastroBody}>
      <div
        className={`${styles.container} ${isRightPanelActive ? styles.rightPanelActive : ""}`}
        id="container"
      >
        {/* Sign Up Form */}
        <div className={`${styles.formContainer} ${styles.signUpContainer}`}>
          <form className={styles.cadastroForm} onSubmit={cadastrar}>
            <h1 style={{ marginBottom: "40px" }}>Criar Conta</h1>
            <input
              className={styles.cadastroInput}
              type="text"
              placeholder="Name"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
            <input
              className={styles.cadastroInput}
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            <button type="submit" className={styles.cadastroButton}>
              Cadastrar
            </button>
          </form>
        </div>

        {/* Sign In Form */}
        <div className={`${styles.formContainer} ${styles.signInContainer}`}>
          <form className={styles.cadastroForm} onSubmit={entrar}>
            <h1 style={{ marginBottom: "40px" }}>Entrar</h1>
            <input
              className={styles.cadastroInput}
              type="text"
              placeholder="Usuário"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
            <input
              className={styles.cadastroInput}
              type="password"
              placeholder="Senha"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            <button type="submit" className={styles.cadastroButton}>
              Entrar
            </button>
          </form>
        </div>

        {erro && <p role="alert">{erro}</p>}

        {/* Overlay Container */}
        <div className={styles.overlayContainer}>
          <div className={styles.overlay}>
            <div className={`${styles.overlayPanel} ${styles.overlayLeft}`}>
              <h1 style={{ marginBottom: "40px" }}>Bem vindo!</h1>
              <p>Coloque seus dados e entre na sua conta!</p>
              <button
                className={`${styles.cadastroButton} ${styles.ghost}`}
                onClick={() => setIsRightPanelActive(false)}
              >
                Entrar
              </button>
            </div>
            <div className={`${styles.overlayPanel} ${styles.overlayRight}`}>
              <h1 style={{ marginBottom: "40px" }}>Bem vindo!</h1>
              <p>Coloque seus dados e descubra novos pratos</p>
              <button
                className={`${styles.cadastroButton} ${styles.ghost}`}
                onClick={() => setIsRightPanelActive(true)}
              >
                Cadastrar
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Cadastro;
