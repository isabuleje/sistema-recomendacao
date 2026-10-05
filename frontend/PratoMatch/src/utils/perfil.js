/*
Gera duas inicias a partir do nome
tipo: luis inácio lula da silva
fica: LI
 */
export function gerarIniciais(nome = "") {
  return nome
    .trim()
    .split(/\s+/)
    .slice(0, 2)
    .map((parte) => parte[0]?.toUpperCase() ?? "")
    .join("");
}
