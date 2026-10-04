/*
import { createRoot } from 'react-dom/client';
Api.js é apenas para função apiFetch e prepararCsrf
  - Função que vai ser reutilizada em todos os outros arquivos service
  - Função necessária para alterar dados (POST, PUT, PATCH e DELETE)
*/

const apiHost = window.location.hostname || "127.0.0.1";
export const API_URL = `http://${apiHost}:8000/api`;

/*Função auxiliar:
  - Para não precisar escrever https://127... TODA VEZ 
  - Credenciais (maioria das requisições precisam)
  - Cookies 
  - Tratamento de erros e conversão da resposta para JSON
*/
export async function apiFetch(endpoint, options = {}) {
  const response = await fetch(`${API_URL}${endpoint}`, {
    credentials: "include",
    ...options,
  });

  let data = null;
  try {
    data = await response.json();
  } catch {
    // Algumas respostas podem não possuir JSON
  }
  if (!response.ok) {
    throw new Error(
      data?.erro ||
        data?.detail ||
        "Ocorreu um erro na comunicação com o servidor.",
    );
  }
  return data;
}

/*
O CSRF é basicamente um mecanismo de segurança 
Ele se certifica que sites maliciosos mexam nos requests como se fossem users autenticado
Ele só é chamado em POST, PUT, PATCH e DELETE
*/

export async function prepararCsrf() {
  await apiFetch("/csrf/");

  const cookie = document.cookie
    .split("; ")
    .find((item) => item.startsWith("csrftoken="));

  if (!cookie) {
    throw new Error("Não foi possível obter o token CSRF");
  }

  return decodeURIComponent(cookie.split("=")[1]);
}
