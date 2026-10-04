const imagens = import.meta.glob(
  "../assets/Pratos/*.{jpg,jpeg,png,webp}",
  {
    eager: true,
    query: "?url",
    import: "default",
  }
);

const listaImagens = Object.values(imagens);

export function imagemAleatoria() {
  if (listaImagens.length === 0) {
    return "/Pratos/pizzar.jpg";
  }

  const indice = Math.floor(Math.random() * listaImagens.length);

  return listaImagens[indice];
}

export function imagemDoPrato(pratoId) {
  if (listaImagens.length === 0) {
    return "/Pratos/pizzar.jpg";
  }

  const id = Number(pratoId);
  const indice = Number.isFinite(id)
    ? Math.abs(id) % listaImagens.length
    : 0;

  return listaImagens[indice];
}