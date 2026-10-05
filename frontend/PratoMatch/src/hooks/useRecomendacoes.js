import { useEffect, useState } from "react";

import { buscarRecomendados } from "../services/recomendacaoService.js";

// Carrega as recomendações do usuário
export function useRecomendacoes() {
    const [pratos, setPratos] = useState([]);
    const [carregando, setCarregando] = useState(true);
    const [erro, setErro] = useState(null);

    useEffect(() => {
        async function carregar() {
            try {
                setCarregando(true);
                setErro(null);

                const dados = await buscarRecomendados();

                setPratos(Array.isArray(dados) ? dados : []);
            } catch (error) {
                console.error("Erro ao carregar recomendações:", error);

                setErro("Não foi possível carregar os pratos.");
            } finally {
                setCarregando(false);
            }
        }

        carregar();
    }, []);

    return {
        pratos,
        carregando,
        erro,
    };
}