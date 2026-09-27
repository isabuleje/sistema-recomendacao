import { useState } from "react";
import { useNavigate } from "react-router-dom";

function Cadastro() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const navigate = useNavigate();

  const cadastrar = async () => {
    try {
      const resposta = await fetch(
        "http://127.0.0.1:8000/api/cadastro/",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          credentials: "include",
          body: JSON.stringify({
            username,
            password,
          }),
        }
      );

      const dados = await resposta.json();

      if (!resposta.ok) {
        throw new Error(dados.erro || "Erro no cadastro.");
      }

      console.log("Usuário criado:", dados);

      navigate("/OnBoarding");
    } catch (erro) {
      console.error("Erro no cadastro:", erro);
    }
  };

  return (
    <div>
      <input
        type="text"
        placeholder="Nome de usuário"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />

      <input
        type="password"
        placeholder="Senha"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />

      <button onClick={cadastrar}>
        Criar conta
      </button>
    </div>
  );
}

export default Cadastro;