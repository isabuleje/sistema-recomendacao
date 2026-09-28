const apiHost = window.location.hostname || "127.0.0.1";

export const API_URL = `http://${apiHost}:8000/api`;

export async function prepararCsrf() {
  await fetch(`${API_URL}/csrf/`, {
    credentials: "include",
  });

  const cookie = document.cookie
    .split("; ")
    .find((item) => item.startsWith("csrftoken="));

  return cookie ? decodeURIComponent(cookie.split("=")[1]) : "";
}
