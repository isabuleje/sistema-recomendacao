//Página para o OnBoarding, onde o usuário vai escolher no mínimo 3 pratos interessantes para não haver o ColdStart e escolher se tem alergias ou algum tipo de restrição aliementar
import CardPrato from '../components/OnBoarding/CardPrato.jsx'
import "../components/OnBoarding/CardPrato.css"

const OnBoarding = () => {
  return (
    //Primeira seção onde vai escolher três pratos interessantes
    <section id="onboarding">
      <section className="pratos-container">
        <h2>Escolha no mínimo 3 pratos de seu interesse</h2>

        <div className="pratos-grid">
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

export default OnBoarding