function PerfilTags({ itens, tipo }) {
  if (!itens.length) {
    return null;
  }

  return (
    <ul className="perfil-tags">
      {itens.map((item) => (
        <li key={item} className={`tag tag-${tipo}`}>
          {item}
        </li>
      ))}
    </ul>
  );
}

export default PerfilTags;
