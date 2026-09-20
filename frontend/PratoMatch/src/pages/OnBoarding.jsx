//Página para o OnBoarding, onde o usuário vai escolher no mínimo 3 pratos interessantes para não haver o ColdStart e escolher se tem alergias ou algum tipo de restrição aliementar
import CardPrato from '../components/OnBoarding/CardPrato.jsx'


const OnBoarding = () => {
  return (
    //Primeira seção onde vai escolher três pratos interessantes
    <section id="onboarding">
      <section>
        <h2>Escolha no mínimo 3 pratos de seu interess </h2>

        <CardPrato name="Prato 1" image="../public/Pratos/prato1.webp" />
        <CardPrato name="Prato 2" image="../public/Pratos/prato2.webp" />
        <CardPrato name="Prato 3" image="../public/Pratos/prato3.webp" />

      </section>
      

      //Segunda seção onde vai escolher se tem alergias ou algum tipo de restrição alimentar
      <section>
      </section>
    </section>
    )
}

export default OnBoarding