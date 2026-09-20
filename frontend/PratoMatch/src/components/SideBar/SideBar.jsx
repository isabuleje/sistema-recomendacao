import { useState } from "react";
import diningImage from "../../assets/dining.png";
import "./SideBar.css";

const menuItems = [
  { label: "Home", icon: "bx  bx-home", },
  { label: "Histórico", icon: "bx bx-history",},
  { label: "Favoritos", icon: "bx bx-heart" },
  { label: "Perfil", icon: "bx bx-user" },
];

const SideBar = () => {
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [openMenu, setOpenMenu] = useState("Category");

  const toggleMenu = (label) => {
    setOpenMenu((currentMenu) => (currentMenu === label ? "" : label));
  };

  return (
    <aside className={`sidebar${isCollapsed ? " close" : ""}`}>
      <div className="logo-details">
        <img src={diningImage} alt="PratoMatch Logo" className="logo_image" />
        <span className="logo_name">PratoMatch</span>
        <button
          className="sidebar-toggle"
          type="button"
          aria-label={isCollapsed ? "Expandir menu" : "Recolher menu"}
          aria-expanded={!isCollapsed}
          onClick={() => setIsCollapsed((collapsed) => !collapsed)}
        >
          <i className="bx bx-menu" aria-hidden="true" />
        </button>
      </div>

      <ul className="nav-links">
        {menuItems.map((item) => {
          const hasChildren = item.children?.length > 0;
          const isOpen = openMenu === item.label;

          return (
            <li className={isOpen ? "active showMenu" : ""} key={item.label}>
              <div className={"menu-link"}>
                <a href="#" onClick={(event) => event.preventDefault()}>
                  <i className={`bx ${item.icon}`} aria-hidden="true" />
                  <span className="link_name">{item.label}</span>
                </a>
              </div>
          
            </li>
          );
        })}
      </ul>
    </aside>
  );
};

export default SideBar;
