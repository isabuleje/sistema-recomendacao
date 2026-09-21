import "./Cards.css";


//na descrição eu imagino que vai ter a categoria do prato, avaliação, tempo de preparo. 
const Card = ({ image, title, description }) => {
  return (
    <div className="card">
        <div className="card-inner">
            <div className="card-front">
                <img src={image} alt={title} className="card-image" />
                <h2>{title}</h2>
            </div>
            <div className="card-back">    
                <p>{description}</p>
            </div>
        </div>
    </div>
  );
};

export default Card;