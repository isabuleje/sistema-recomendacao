import { useState, useEffect } from "react";
import { salvarFavoritos } from "../services/Pratos.js";
import { buscarPratoFavoritados } from "../services/favoritosService.js";

//Alterna favoritos e salva favorito

export function useFavoritos(pratoId, favoritoInicial = false) {
  const [favorito, setFavorito] = useState(Boolean(favoritoInicial));
  const [carregando, setCarregando] = useState(false);
  const [salvando, setSalvando] = useState(false);
  const [erro, setErro] = useState("");

  useEffect(() => {
    async function carregar() {
      try {
        setCarregando(true);

        const dados = await buscarPratoFavoritados();

        const ids = dados.map((prato) => prato.id);

        setFavorito(new Set(ids));
      } catch (error) {
        // Favoritos não devem impedir a Home de funcionar.
        console.error("Erro ao carregar favoritos:", error);
      } finally {
        setCarregando(false);
      }
    }

    carregar();
  }, []);

  const alternar = async () => {
    if (salvando) {
      return;
    }

    const anterior = favorito;
    const novo = !anterior;

    setFavorito(novo);
    setSalvando(true);
    setErro("");

    try {
      await salvarFavoritos(pratoId, novo);
    } catch (error) {
      //deu erro ent volta ao estado anterior
      setFavorito(anterior);
      setErro(error.message || "Erro ao atualizar favorito.");
    } finally {
      //independente de ter dado certo ou errado, vai setar salvando como false
      setSalvando(false);
    }
  };

  return { favorito, alternar, salvando, erro, carregando };
}
