//Página do Histórico, onde o usuário vai poder ver os pratos que ele já avaliou e as avaliações que ele deu para cada prato
import "../components/Home/Placa.css";

const Historico = () => {
  return (
    <div className="home-page">
      <div className="user-greeting">
        <p style={{ color: "#055746", fontWeight: "700" }}> Olá, usuário! 👋</p>
        <i class="bx bx-user" style={{ color: "#000504" }} />
      </div>

      <div className="placa">
        <div className="placa-conteudo">
          <h2 className="placa-texto">Seu histórico</h2>

          <p className="placa-subtitulo">
            Aqui estão os pratos que você já avaliou ou visualizou.
          </p>
        </div>
      </div>
    </div>
  );
};

export default Historico;
