import { BrowserRouter, Routes, Route } from "react-router-dom";

import MainLayout from "./layouts/MainLayout.jsx";

import Home from "./pages/Home";


export default function App() {
  return (
    <BrowserRouter>
      <MainLayout>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/historico" element={<h1>Histórico</h1>} />
          <Route path="/favoritos" element={<h1>Favoritos</h1>} />
          <Route path="/perfil" element={<h1>Perfil</h1>} />
        </Routes>
      </MainLayout>
    </BrowserRouter>
  );
}