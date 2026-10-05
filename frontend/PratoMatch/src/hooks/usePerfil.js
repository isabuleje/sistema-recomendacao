import { useEffect, useState } from "react";

import { buscarPerfil } from "../services/perfilService.js";

// Disponibiliza os dados do perfil
export function usePerfil() {
    const [perfil, setPerfil] = useState(null);
    const [carregando, setCarregando] = useState(true);
    const [erro, setErro] = useState(null);

    useEffect(() => {
        async function carregar() {
            try {
                setCarregando(true);
                setErro(null);

                const dados = await buscarPerfil();

                setPerfil(dados);
            } catch (error) {
                console.error("Erro ao carregar perfil:", error);

                setErro("Não foi possível carregar seu perfil.");
            } finally {
                setCarregando(false);
            }
        }

        carregar();
    }, []);

    return {
        perfil,
        carregando,
        erro,
    };
}