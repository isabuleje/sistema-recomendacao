import "./ShadowText.css";

// Reaproveita o mesmo efeito de texto em qualquer parte da aplicação.
const ShadowText = ({ children, className = "", main_color, second_color }) => {
  return (
    <span className={`shadow-text ${className}`}>
      {/* A camada escura fica atrás e cria o efeito de profundidade. */}
      <span className="shadow-text__back" style={{ color: second_color }} aria-hidden="true">
        {children}
      </span>
      {/* Esta é a camada principal, lida pelo leitor de tela. */}
      <span className="shadow-text__front" style={{ color: main_color }}>
        {children}
      </span>
    </span>
  );
};

export default ShadowText;
