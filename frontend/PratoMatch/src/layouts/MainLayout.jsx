import Sidebar from "../components/SideBar/SideBar.jsx";
import { useLocation } from "react-router-dom";

export default function MainLayout({ children }) {
  const { pathname } = useLocation();
  const mostrarSidebar = pathname !== "/";

  return (
    <div className={`app-layout${mostrarSidebar ? "" : " no-sidebar"}`}>
      {mostrarSidebar && <Sidebar />}

      <main className="main-content">{children}</main>
    </div>
  );
}
