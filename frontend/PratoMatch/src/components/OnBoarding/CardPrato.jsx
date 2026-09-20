import "./CardPrato.css";

const CardPrato = ({name, image}) => {
  return (
    <div > 
        <div class="card_img"> 
            <img src={image} alt="user-image"/>
        </div>
        <div class="card_info"> 
            <h2>{name}</h2>
            <a href="#!">hello</a>
        </div>
    </div>
    )
}

export default CardPrato

  