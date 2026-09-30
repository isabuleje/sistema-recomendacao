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
    console.log("Tá contando como se fosse zero")
    return "/Pratos/pizzar.jpg";
  }

  const indice = Math.floor(Math.random() * listaImagens.length);

  return listaImagens[indice];
}