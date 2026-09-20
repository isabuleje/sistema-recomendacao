/*
Página dividida em 3 partes:
1. Selecionar se possui algum tipo de alergia ou restrição alimentar
2. Escolher no mínimo 3 pratos de interesse
3. Confirmar as preferências selecionadas

*/
import CardPrato from '../components/OnBoarding/CardPrato.jsx'
import "../components/OnBoarding/CardPrato.css"

const OnBoarding = () => {
  return (
    //Primeira seção onde vai escolher três pratos interessantes
    <section id="onboarding">
      <section className="pratos-container">
        <h2>Escolha no mínimo 3 pratos de seu interesse</h2>

        <div className="pratos-grid" style={{  marginTop: "100px"}}>
          <CardPrato name="Prato 1" image="../public/Pratos/prato1.webp" />
          <CardPrato name="Prato 2" image="../public/Pratos/prato2.webp" />
          <CardPrato name="Prato 3" image="../public/Pratos/prato3.webp" />
          <CardPrato name="Prato 4" image="../public/Pratos/prato4.webp" />
          <CardPrato name="Prato 5" image="../public/Pratos/prato5.webp" />
          <CardPrato name="Prato 6" image="../public/Pratos/prato6.webp" />
        </div>
      </section>
      

      //Segunda seção onde vai escolher se tem alergias ou algum tipo de restrição alimentar
      <section>
      </section>
    </section>
    )
}


const RestricaoAlimentar = () => {
  return (
    <section className="restricao-container">
      <h2>Antes de começar conte-nos sobre sua alimentação</h2>
      <p> Assim, as recomendações ficam mais seguras e do seu estilo de vida.</p>

      <h6>Você tem alguma restrição alimentar?</h6>
      




    </section>
  )
};
export default OnBoarding