import { useCallback, useEffect, useState } from "react";

import { buscarRecomendados } from "../services/recomendacaoService.js";
import {
    deveAtualizarRecomendacoes,
    limparAvaliacoesPendentes,
} from "../utils/atualizacaoRecomendacoes.js";

// Carrega as recomendações do usuário
export function useRecomendacoes() {
    const [pratos, setPratos] = useState([]);
    const [carregando, setCarregando] = useState(true);
    const [erro, setErro] = useState(null);

    const carregar = useCallback(async (limparContador = false) => {
        try {
            setCarregando(true);
            setErro(null);

            const dados = await buscarRecomendados();

            setPratos(Array.isArray(dados) ? dados : []);
            if (limparContador) {
                limparAvaliacoesPendentes();
            }
        } catch (error) {
            console.error("Erro ao carregar recomendações:", error);

            setErro("Não foi possível carregar os pratos.");
        } finally {
            setCarregando(false);
        }
    }, []);

    useEffect(() => {
        async function carregarInicial() {
            await carregar(deveAtualizarRecomendacoes());
        }

        carregarInicial();

        const atualizarDepoisDeCincoAvaliacoes = () => {
            if (deveAtualizarRecomendacoes()) {
                carregar(true);
            }
        };

        window.addEventListener(
            "avaliacao-salva",
            atualizarDepoisDeCincoAvaliacoes,
        );

        return () => {
            window.removeEventListener(
                "avaliacao-salva",
                atualizarDepoisDeCincoAvaliacoes,
            );
        };
    }, [carregar]);

    return {
        pratos,
        carregando,
        erro,
    };
}