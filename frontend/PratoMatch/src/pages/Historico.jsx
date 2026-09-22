//Página do Histórico, onde o usuário vai poder ver os pratos que ele já avaliou e as avaliações que ele deu para cada prato
import "../components/Historico/Card.module.css";
import Card from "../components/Historico/Card.jsx";

const Historico = () => {
  return (
    <div className="home-page">
      <div className="user-greeting">
        <p style={{ color: "#055746", fontWeight: "700" }}> Olá, usuário! 👋</p>
        <i className="bx bx-user" style={{ color: "#000504" }} />
      </div>

      <div>
        <button> Historico </button>
        <button> Favoritos</button>
      </div>

      <Card
        titulo="Pizza Margherita"
        descricao="Massa artesanal, molho de tomate, mussarela de búfala e manjericão fresco."
        imagem="https://images.unsplash.com/photo-1574071318508-1cdbab80d002?auto=format&fit=crop&q=80&w=400"
        tempo="25 min"
        nota="4,8"
        numerosNota="(1,2k)"
        data="21 de setembro de 2025"
      />

      <Card
        titulo="Pizza Margherita"
        descricao="Massa artesanal, molho de tomate, mussarela de búfala e manjericão fresco."
        imagem="https://images.unsplash.com/photo-1574071318508-1cdbab80d002?auto=format&fit=crop&q=80&w=400"
        tempo="25 min"
        nota="4,8"
        numerosNota="(1,2k)"
        data="21 de setembro de 2025"
      />

      <Card
        titulo="Pizza Margherita"
        descricao="Massa artesanal, molho de tomate, mussarela de búfala e manjericão fresco."
        imagem="https://images.unsplash.com/photo-1574071318508-1cdbab80d002?auto=format&fit=crop&q=80&w=400"
        tempo="25 min"
        nota="4,8"
        numerosNota="(1,2k)"
        data="21 de setembro de 2025"
      />

      <Card
        titulo="Pizza Margherita"
        descricao="Massa artesanal, molho de tomate, mussarela de búfala e manjericão fresco."
        imagem="https://images.unsplash.com/photo-1574071318508-1cdbab80d002?auto=format&fit=crop&q=80&w=400"
        tempo="25 min"
        nota="4,8"
        numerosNota="(1,2k)"
        data="21 de setembro de 2025"
      />

      <Card
        titulo="Pizza Margherita"
        descricao="Massa artesanal, molho de tomate, mussarela de búfala e manjericão fresco."
        imagem="https://images.unsplash.com/photo-1574071318508-1cdbab80d002?auto=format&fit=crop&q=80&w=400"
        tempo="25 min"
        nota="4,8"
        numerosNota="(1,2k)"
        data="21 de setembro de 2025"
      />

      <Card
        titulo="Pizza Margherita"
        descricao="Massa artesanal, molho de tomate, mussarela de búfala e manjericão fresco."
        imagem="https://images.unsplash.com/photo-1574071318508-1cdbab80d002?auto=format&fit=crop&q=80&w=400"
        tempo="25 min"
        nota="4,8"
        numerosNota="(1,2k)"
        data="21 de setembro de 2025"
      />
    </div>
  );
};

export default Historico;
