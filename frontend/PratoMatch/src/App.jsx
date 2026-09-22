import { BrowserRouter, Routes, Route } from "react-router-dom";

import MainLayout from "./layouts/MainLayout.jsx";

import Home from "./pages/Home";
import Perfil from "./pages/Perfil";
import Historico from "./pages/Historico";
import OnBoarding from "./pages/OnBoarding.jsx";
import Favorito from "./pages/Favorito.jsx";

export default function App() {
  return (
    <BrowserRouter>
      <MainLayout>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/historico" element={<Historico />} />
          <Route path="/favoritos" element={<Favorito />} />
          <Route path="/perfil" element={<Perfil />} />
          <Route path="/onboarding" element={<OnBoarding />} />
        </Routes>
      </MainLayout>
    </BrowserRouter>
  );
}
