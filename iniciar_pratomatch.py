import os
import sys
import subprocess
from pathlib import Path


# ============================================================
# CONFIGURAÇÃO
# ============================================================

ROOT = Path(__file__).resolve().parent

BACKEND = ROOT / "backend"
DJANGO = BACKEND / "PratoMatch"

FRONTEND = ROOT / "frontend" / "PratoMatch"

VENV = BACKEND / "venv"
PYTHON = VENV / "Scripts" / "python.exe"


# ============================================================
# FUNÇÕES
# ============================================================

def executar(comando, pasta):
    print(f"\n> Executando: {comando}")
    print(f"> Pasta: {pasta}\n")

    return subprocess.run(
        comando,
        cwd=pasta,
        shell=True
    )


def criar_venv():
    if not VENV.exists():
        print("\nCriando ambiente virtual...\n")

        subprocess.run(
            [sys.executable, "-m", "venv", str(VENV)],
            check=True
        )

    else:
        print("\nAmbiente virtual já existe.")


def instalar_requirements():
    arquivos = list(BACKEND.rglob("requirements*.txt"))

    if not arquivos:
        print("\nNenhum requirements.txt encontrado.")
        return

    print("\nRequirements encontrados:")

    for arquivo in arquivos:
        print(f" - {arquivo}")

    for arquivo in arquivos:
        print(f"\nInstalando {arquivo.name}...\n")

        subprocess.run(
            [
                str(PYTHON),
                "-m",
                "pip",
                "install",
                "-r",
                str(arquivo)
            ],
            check=True
        )


def instalar_frontend():
    node_modules = FRONTEND / "node_modules"

    if not node_modules.exists():

        print("\nnode_modules não encontrado.")
        print("Executando npm install...\n")

        executar(
            "npm install",
            FRONTEND
        )

    else:
        print("\nnode_modules já existe.")


# ============================================================
# INÍCIO
# ============================================================

print("=" * 60)
print("             PRATOMATCH")
print("        Inicialização do sistema")
print("=" * 60)


# 1. Criar ambiente virtual
criar_venv()


# 2. Instalar requirements
instalar_requirements()


# 3. Instalar dependências do frontend
instalar_frontend()


# ============================================================
# INICIAR SERVIDORES
# ============================================================

print("\n")
print("=" * 60)
print("Iniciando Django...")
print("=" * 60)

django = subprocess.Popen(
    [
        str(PYTHON),
        "manage.py",
        "runserver"
    ],
    cwd=DJANGO
)


print("\n")
print("=" * 60)
print("Iniciando Frontend...")
print("=" * 60)

frontend = subprocess.Popen(
    "npm run dev",
    cwd=FRONTEND,
    shell=True
)


print("\n")
print("=" * 60)
print("PRATOMATCH INICIADO!")
print("=" * 60)

print("\nDjango:")
print("http://127.0.0.1:8000")

print("\nFrontend:")
print("Verifique a URL exibida pelo Vite.")

print("\nFeche esta janela para encerrar os servidores.\n")


try:
    django.wait()
    frontend.wait()

except KeyboardInterrupt:

    print("\nEncerrando PratoMatch...")

    django.terminate()
    frontend.terminate()