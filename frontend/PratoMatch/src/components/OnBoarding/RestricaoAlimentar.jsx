import "./RestricaoAlimentarCard.css";

const RestricaoAlimentarCard = ({name, icon}) => {
return(
    <div className="restricao_card">
        <div className="card_img">
            <img src={icon} alt="user-image"/>
        </div>
        <div className="card_info">
            <h2>{name}</h2>
        </div>
    </div>
)
}