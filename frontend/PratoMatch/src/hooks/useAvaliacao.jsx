import { useEffect, useState } from "react";
import { salvarAvaliacao } from "../services/Pratos.js";

export function useAvaliacao(pratoId, notaInicial = 0) {
  const [nota, setNota] = useState(Number(notaInicial) || 0);
  const [salvando, setSalvando] = useState(false);
  const [erro, setErro] = useState("");

  useEffect(() => {
    setNota(Number(notaInicial) || 0);
  }, [pratoId, notaInicial]);

  const avaliar = async (novaNota) => {
    const notaAnterior = nota;
    setNota(novaNota);
    setSalvando(true);
    setErro("");

    try {
      const resposta = await salvarAvaliacao(pratoId, novaNota);
      setNota(resposta.nota);
      return resposta;
    } catch (error) {
      setNota(notaAnterior);
      setErro(error.message);
      throw error;
    } finally {
      setSalvando(false);
    }
  };

  return { nota, avaliar, salvando, erro };
}
