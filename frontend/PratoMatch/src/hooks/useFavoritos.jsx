import { useState, useEffect } from "react";
import { buscarFavoritos, salvarFavorito } from "../services/favoritosService.js";

//Alterna favoritos e salva favorito

export function useFavoritos(pratoId, favoritoInicial = false) {
  const usaColecao = pratoId == null;
  const [favorito, setFavorito] = useState(() =>
    usaColecao ? new Set() : Boolean(favoritoInicial),
  );
  const [carregando, setCarregando] = useState(false);
  const [salvando, setSalvando] = useState(false);
  const [erro, setErro] = useState("");

  useEffect(() => {
    async function carregar() {
      try {
        setCarregando(true);

        const dados = await buscarFavoritos();

        const pratos = Array.isArray(dados) ? dados : (dados?.pratos ?? []);
        const ids = pratos.map((prato) => prato.id);

        setFavorito(usaColecao ? new Set(ids) : ids.includes(pratoId));
      } catch (error) {
        // Favoritos não devem impedir a Home de funcionar.
        console.error("Erro ao carregar favoritos:", error);
      } finally {
        setCarregando(false);
      }
    }

    carregar();
  }, [pratoId, usaColecao]);

  const alternar = async (id = pratoId) => {
    if (salvando) {
      return;
    }

    if (id == null) {
      const erroId = new Error("Não foi possível identificar o prato.");
      setErro(erroId.message);
      return;
    }

    const anterior = favorito;
    const estaFavorito = usaColecao ? anterior.has(id) : anterior;
    const novo = !estaFavorito;

    setFavorito(
      usaColecao
        ? new Set(
            novo
              ? [...anterior, id]
              : [...anterior].filter((favoritoId) => favoritoId !== id),
          )
        : novo,
    );
    setSalvando(true);
    setErro("");

    try {
      await salvarFavorito(id, novo);
    } catch (error) {
      //deu erro ent volta ao estado anterior
      setFavorito(anterior);
      setErro(error.message || "Erro ao atualizar favorito.");
    } finally {
      //independente de ter dado certo ou errado, vai setar salvando como false
      setSalvando(false);
    }
  };

  return {
    favorito,
    favoritos: usaColecao ? favorito : new Set(favorito ? [pratoId] : []),
    alternar,
    alternarFavorito: alternar,
    salvando,
    erro,
    carregando,
  };
}
