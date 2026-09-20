import { useState } from "react";
import { NavLink, useLocation } from "react-router-dom";
import diningImage from "../../assets/dining.png";
import ShadowText from "../ShadowText/ShadowText";
import "./SideBar.css";

const menuItems = [
  { label: "Home", icon: "bx-home", path: "/" },
  { label: "Histórico", icon: "bx-history", path: "/historico" },
  { label: "Favoritos", icon: "bx-heart", path: "/favoritos" },
];
const profileItem = { label: "Perfil", icon: "bx-user", path: "/perfil" };

const SideBar = () => {
  // Controla se a sidebar mostra apenas os ícones ou também os nomes.
  const [isCollapsed, setIsCollapsed] = useState(false);
  const location = useLocation();

  return (
    <aside className={`sidebar${isCollapsed ? " close" : ""}`}>
      <div className="logo-details">
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
                  <ShadowText className="link_name" main_color={"#ffbf00"} second_color={"#c45019"}>
                    {item.label}
                  </ShadowText>
                </NavLink>
              </div>
          
            </li>
          );
        })}
      </ul>

      {/* Perfil fica separado no rodapé para não se misturar às categorias principais. */}
      <ul className="profile-link">
        <li className={location.pathname === profileItem.path ? "active" : ""}>
          <NavLink to={profileItem.path}>
            <i className={`bx ${profileItem.icon}`} aria-hidden="true" />
            <ShadowText className="link_name" main_color="#ffbf00" second_color="#c45019">
              {profileItem.label}
            </ShadowText>
          </NavLink>
        </li>
      </ul>

      {/* Controle circular no meio da borda: compacto e separado da logo. */}
      <button
        className="sidebar-collapse-toggle"
        type="button"
        aria-label={isCollapsed ? "Expandir menu" : "Recolher menu"}
        aria-expanded={!isCollapsed}
        onClick={() => setIsCollapsed((collapsed) => !collapsed)}
      >
        <i className={`bx ${isCollapsed ? "bx-chevron-right" : "bx-chevron-left"}`} aria-hidden="true" />
      </button>
    </aside>
  );
};

export default SideBar;
