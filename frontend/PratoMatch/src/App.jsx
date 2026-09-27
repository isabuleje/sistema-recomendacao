import { useState } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";

import MainLayout from "./layouts/MainLayout.jsx";

import Home from "./pages/Home";
import Perfil from "./pages/Perfil";
import Historico from "./pages/Historico";
import OnBoarding from "./pages/OnBoarding.jsx";
import Favorito from "./pages/Favorito.jsx";
import CardDetalhesPage from "./pages/CardDetalhesPage.jsx";
import Cadastro from "./pages/Cadastro.jsx";

export default function App() {
  const [favoritos, setFavoritos] = useState([]);

  const alternarFavorito = (prato) => {
    setFavoritos((atuais) => {
      const jaFavoritado = atuais.some((favorito) => favorito.id === prato.id);

      return jaFavoritado
        ? atuais.filter((favorito) => favorito.id !== prato.id)
        : [...atuais, prato];
    });
  };

  return (
    <BrowserRouter>
      <MainLayout>
        <Routes>
          <Route
            path="/home"
            element={
              <Home favoritos={favoritos} alternarFavorito={alternarFavorito} />
            }
          />
          <Route
            path="/historico"
            element={
              <Historico
                favoritos={favoritos}
                alternarFavorito={alternarFavorito}
              />
            }
          />
          <Route
            path="/favoritos"
            element={
              <Favorito
                favoritos={favoritos}
                alternarFavorito={alternarFavorito}
              />
            }
          />
          <Route path="/perfil" element={<Perfil />} />
          <Route path="/onboarding" element={<OnBoarding />} />
          <Route path="/pratos/:id" element={<CardDetalhesPage />} />
          <Route path="/" element={<Cadastro />} />
        </Routes>
      </MainLayout>
    </BrowserRouter>
  );
}
