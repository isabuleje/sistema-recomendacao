import { useState } from "react";
import { salvarFavoritos } from "../services/Pratos.js";

export function useFavoritos(pratoId, favoritoInicial = false) {
  const [favorito, setFavorito] = useState(Boolean(favoritoInicial));
  const [salvando, setSalvando] = useState(false);
  const [erro, setErro] = useState("");

  const alternar = async () => {
    if (salvando) return;

    const anterior = favorito;
    const novo = !anterior;

    setFavorito(novo); 
    setSalvando(true);
    setErro("");

    try {
      await salvarFavoritos(pratoId, novo);
    } catch (error) {
      setFavorito(anterior); 
      setErro(error.message);
    } finally {
      setSalvando(false);
    }
  };

  return { favorito, alternar, salvando, erro };
}