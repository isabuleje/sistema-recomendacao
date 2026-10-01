import { useState } from "react";
import { salvarAvaliacao } from "../services/avaliacaoService.js";

/*Hook responsável por gerenciar a avaliação de um prato*/
export function useAvaliacao(pratoId, notaInicial = 0) {
  const [nota, setNota] = useState(notaInicial ? Number(notaInicial) : null); /*number é pra caso a nota venha como string, ela vira numero*/
  const [salvando, setSalvando] = useState(false);
  const [erro, setErro] = useState("");

  const avaliar = async (novaNota) => {

    if (!Number.isInteger(novaNota) || novaNota < 1 || novaNota > 5) {
      setErro("A avaliação deve estar entre 1 e 5.");
      return;
    }


    if (salvando) return; //se já estiver salvando, não faz nada
    const notaAnterior = nota; //caso de erro, salva a nota anterior
    setNota(novaNota);
    setSalvando(true);
    setErro("");


    try {
      const resposta = await salvarAvaliacao(
        pratoId,
        novaNota
      );

      setNota(resposta.nota);
      return resposta;
    } 
    catch (error) {
      setNota(notaAnterior);
      setErro(error.message);
      throw error;
    } 
    finally {
      setSalvando(false);
    }
  };

  return { nota, avaliar, salvando, erro };
}
