// Página inicial, onde o usuário vai poder ver os pratos recomendados, pratos populares e novidades
import ShadowText from "../components/ShadowText/ShadowText";
import "../components/Home/Placa.css";
import { Search, Send } from "lucide-react";
import Card from "../components/Home/Card";

const Home = () => {
  return (
    <div>
      <div className="placa">
        <div className="placa-interna">
          <div  className="placa-texto">
             <ShadowText  main_color={"#ffbf00"} second_color={"#c45019"}>
          Descubra pratos incríveis e avalie suas experiências gastronômicas! 
        </ShadowText>
          </div>
        
    </div>

      </div>

      <section margin-left="80px">
        <div className="input-wrapper">
          <Search className="search-icon" />

          <input
            type="text"
            placeholder="O que você quer comer hoje?"
            name="text"
            className="input"
          />

          <button className="send-button">
            <Send />
          </button>
        </div>
      </section>

        <ShadowText main_color={"#ffbf00"} second_color={"#c45019"} >
             Pratos recomendados baseados no seu perfil
        </ShadowText>

        <div className="cards-container">
          <Card title="Prato 1" description="Descrição do prato 1" imageUrl="https://via.placeholder.com/150" />
          <Card title="Prato 2" description="Descrição do prato 2" imageUrl="https://via.placeholder.com/150" />
          <Card title="Prato 3" description="Descrição do prato 3" imageUrl="https://via.placeholder.com/150" />
          <Card title="Prato 4" description="Descrição do prato 4" imageUrl="https://via.placeholder.com/150" />
        </div>
      
        <ShadowText main_color={"#ffbf00"} second_color={"#c45019"} >
            Pratos populares 
        </ShadowText>

        <div className="cards-container">
          <Card title="Prato 1" description="Descrição do prato 1" imageUrl="https://via.placeholder.com/150" />
          <Card title="Prato 2" description="Descrição do prato 2" imageUrl="https://via.placeholder.com/150" />
          <Card title="Prato 3" description="Descrição do prato 3" imageUrl="https://via.placeholder.com/150" />
          <Card title="Prato 4" description="Descrição do prato 4" imageUrl="https://via.placeholder.com/150" />
        </div>

        

        <ShadowText main_color={"#ffbf00"} second_color={"#c45019"} >
           Novidades 
        </ShadowText>

        <div className="cards-container">
          <Card title="Prato 1" description="Descrição do prato 1" imageUrl="https://via.placeholder.com/150" />
          <Card title="Prato 2" description="Descrição do prato 2" imageUrl="https://via.placeholder.com/150" />
          <Card title="Prato 3" description="Descrição do prato 3" imageUrl="https://via.placeholder.com/150" />
          <Card title="Prato 4" description="Descrição do prato 4" imageUrl="https://via.placeholder.com/150" />
        </div>

        
    </div>
  );
};

export default Home;