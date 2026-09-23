const OnBoardingHeader = ({ fase, totalFases }) => (
  <header className="onboarding-header">
    <div
      className="onboarding-progresso"
      role="list"
      aria-label={`Fase ${fase} de ${totalFases}`}
    >
      {Array.from({ length: totalFases }, (_, index) => index + 1).map(
        (numero) => (
          <span
            key={numero}
            role="listitem"
            aria-label={`Fase ${numero}`}
            className={
              "progresso-ponto" +
              (numero === fase ? " ativo" : "") +
              (numero < fase ? " concluido" : "")
            }
          />
        ),
      )}
    </div>

    <span className="onboarding-fase-label">
      Fase {fase} de {totalFases}
    </span>
  </header>
);

export default OnBoardingHeader;
