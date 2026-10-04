import { NavLink, useLocation } from "react-router-dom";
import diningImage from "../../assets/dining.png";
import ShadowText from "../common/shadow-text/ShadowText.jsx";
import "./SideBar.css";


const menuItems = [
  { label: "Home", icon: "bx-home", path: "/home" },
  { label: "Histórico", icon: "bx-history", path: "/historico" },
  { label: "Avaliados", icon: "bx-heart", path: "/avaliados" },
]
const profileItem = { label: "Perfil", icon: "bx-user", path: "/perfil" };

const SideBar = () => {
  const location = useLocation();

  return (
    <aside className="sidebar close">
      <div className="logo-details" style={{marginBottom: "30px"}}>
        <img src={diningImage} alt="PratoMatch Logo" className="logo_image" />
        <ShadowText main_color={"#ffbf00"} second_color={"#c45019"} className="logo_name">
          PratoMatch
        </ShadowText>
      </div>

      {/* Cada item é criado a partir da lista acima para manter o menu fácil de editar. */}
      <ul className="nav-links">
        {menuItems.map((item) => {
          const isActive = location.pathname === item.path;

          return (
            <li className={isActive ? "active" : ""} key={item.label}>
              <div className={"menu-link"}>
                <NavLink to={item.path} end={item.path === "/"}>
                  <i className={`bx ${item.icon}`} aria-hidden="true" />
                  <span className="link_name category-label">
                    {item.label}
                  </span>
                </NavLink>
              </div>
          
            </li>
          );
        })}
      </ul>

        {/* DECORAÇÃO DE FOLHAS */}
<div className="sidebar-decoration">
  <svg
    viewBox="0 0 160 250"
    xmlns="http://www.w3.org/2000/svg"
    aria-hidden="true"
  >
    {/* Caule principal */}
    <path
      d="
        M 8 250
        C 5 220, 15 195, 28 175
        C 42 153, 48 130, 55 108
        C 61 88, 68 67, 82 45
      "
    />

    {/* Caule lateral inferior */}
    <path
      d="
        M 15 215
        C 35 205, 55 197, 73 181
        C 87 168, 94 154, 99 140
      "
    />

    {/* Caule lateral superior */}
    <path
      d="
        M 45 145
        C 30 135, 20 125, 18 112
      "
    />

    {/* Folha inferior esquerda */}
    <path
      d="
        M 27 177
        C 5 170, -3 151, 5 134
        C 13 118, 31 113, 43 119
        C 48 137, 43 157, 27 177 Z
      "
    />

    {/* Folha inferior direita */}
    <path
      d="
        M 48 198
        C 52 177, 68 162, 89 163
        C 103 166, 108 178, 106 190
        C 91 202, 69 205, 48 198 Z
      "
    />

    {/* Folha central esquerda */}
    <path
      d="
        M 43 145
        C 24 144, 10 134, 10 119
        C 11 105, 23 96, 38 96
        C 51 105, 53 124, 43 145 Z
      "
    />

    {/* Folha central direita */}
    <path
      d="
        M 60 112
        C 61 94, 75 81, 94 81
        C 108 83, 114 94, 112 106
        C 99 118, 78 120, 60 112 Z
      "
    />

    {/* Folha superior esquerda */}
    <path
      d="
        M 57 92
        C 40 89, 29 79, 30 67
        C 32 55, 43 48, 57 49
        C 68 58, 68 76, 57 92 Z
      "
    />

    {/* Folha superior direita */}
    <path
      d="
        M 76 67
        C 79 51, 92 40, 108 42
        C 119 45, 124 55, 120 66
        C 108 76, 91 76, 76 67 Z
      "
    />

    {/* Detalhes internos das folhas */}
    <path d="M 8 139 C 18 147, 25 158, 27 177" />
    <path d="M 50 196 C 65 188, 80 178, 98 164" />
    <path d="M 12 119 C 24 125, 34 134, 43 145" />
    <path d="M 62 110 C 76 104, 88 95, 94 82" />
    <path d="M 31 68 C 42 74, 51 82, 57 92" />
    <path d="M 77 66 C 91 61, 101 51, 108 43" />
  </svg>
</div>

      {/* Perfil fica separado no rodapé para não se misturar às categorias principais. */}
      <ul className="profile-link">
        <li className={location.pathname === profileItem.path ? "active" : ""}>
          <NavLink to={profileItem.path}>
            <i className={`bx ${profileItem.icon}`} aria-hidden="true" />
            <span className="link_name category-label">
              {profileItem.label}
            </span>
          </NavLink>
        </li>
      </ul>

    </aside>
  );
};

export default SideBar;
