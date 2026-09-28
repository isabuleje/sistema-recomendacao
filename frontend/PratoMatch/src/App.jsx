import { BrowserRouter, Routes, Route } from "react-router-dom";

import MainLayout from "./layouts/MainLayout.jsx";

import Home from "./pages/Home";
import Perfil from "./pages/Perfil";
import Historico from "./pages/Historico";
import OnBoarding from "./pages/OnBoarding.jsx";
import Avaliado from "./pages/Avaliado.jsx";
import CardDetalhesPage from "./pages/CardDetalhesPage.jsx";
import Cadastro from "./pages/Cadastro.jsx";

export default function App() {
  return (
    <BrowserRouter>
      <MainLayout>
        <Routes>
          <Route path="/home" element={<Home />} />
          <Route path="/historico" element={<Historico />} />
          <Route path="/avaliados" element={<Avaliado />} />
          <Route path="/perfil" element={<Perfil />} />
          <Route path="/onboarding" element={<OnBoarding />} />
          <Route path="/pratos/:id" element={<CardDetalhesPage />} />
          <Route path="/" element={<Cadastro />} />
        </Routes>
      </MainLayout>
    </BrowserRouter>
  );
}
