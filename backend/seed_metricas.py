"""Cria uma base demonstrativa isolada para avaliar as métricas."""

import ast
import csv
import sqlite3
from collections import Counter, defaultdict
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
ARQUIVO_RECEITAS = BASE_DIR / "dataset" / "PP_recipes.csv"
BANCO_METRICAS = BASE_DIR / "PratoMatch" / "db_metricas.sqlite3"
QUANTIDADE_USUARIOS = 50
PRATOS_POR_USUARIO = 15
INTERACOES_TREINO = 5


def carregar_receitas():
    receitas = {}
    with ARQUIVO_RECEITAS.open(encoding="utf-8", newline="") as arquivo:
        for linha in csv.DictReader(arquivo):
            ingredientes = ast.literal_eval(linha["ingredient_ids"])
            if ingredientes:
                receitas[int(linha["id"])] = sorted(set(map(int, ingredientes)))
    return receitas


def criar_coortes(receitas):
    frequencias = Counter(
        ingrediente
        for ingredientes in receitas.values()
        for ingrediente in ingredientes
    )
    receitas_por_ingrediente = defaultdict(set)
    for prato_id, ingredientes in receitas.items():
        for ingrediente in ingredientes:
            if frequencias[ingrediente] <= 2000:
                receitas_por_ingrediente[ingrediente].add(prato_id)

    coortes = []
    usadas = set()
    for prato_id, ingredientes_lista in receitas.items():
        if prato_id in usadas:
            continue
        ingredientes = set(ingredientes_lista)
        ingredientes_raros = [
            ingrediente
            for ingrediente in ingredientes
            if frequencias[ingrediente] <= 2000
        ]
        if len(ingredientes_raros) < 2:
            continue

        candidatos = set()
        for ingrediente in ingredientes_raros:
            candidatos.update(receitas_por_ingrediente[ingrediente])
        candidatos.discard(prato_id)

        similares = []
        for candidato in candidatos - usadas:
            ingredientes_candidato = set(receitas[candidato])
            intersecao = len(ingredientes & ingredientes_candidato)
            if intersecao < 2:
                continue
            similaridade = intersecao / len(ingredientes | ingredientes_candidato)
            similares.append((similaridade, candidato))

        grupo = [prato_id] + [
            candidato
            for _, candidato in sorted(similares, reverse=True)[
                : PRATOS_POR_USUARIO - 1
            ]
        ]
        if len(grupo) != PRATOS_POR_USUARIO:
            continue

        coortes.append(grupo)
        usadas.update(grupo)
        if len(coortes) == QUANTIDADE_USUARIOS:
            break

    if len(coortes) != QUANTIDADE_USUARIOS:
        raise RuntimeError(
            "Não foi possível montar coortes suficientes com receitas "
            "que compartilham ingredientes."
        )
    return coortes


def criar_banco():
    receitas = carregar_receitas()
    coortes = criar_coortes(receitas)

    with sqlite3.connect(BANCO_METRICAS) as conexao:
        conexao.executescript(
            """
            DROP TABLE IF EXISTS interacao;
            DROP TABLE IF EXISTS coorte_prato;
            DROP TABLE IF EXISTS prato;
            DROP TABLE IF EXISTS coorte;

            CREATE TABLE coorte (
                id INTEGER PRIMARY KEY,
                usuario_id INTEGER NOT NULL UNIQUE
            );
            CREATE TABLE prato (
                id INTEGER PRIMARY KEY,
                ingredient_ids TEXT NOT NULL
            );
            CREATE TABLE coorte_prato (
                coorte_id INTEGER NOT NULL REFERENCES coorte(id),
                prato_id INTEGER NOT NULL REFERENCES prato(id),
                PRIMARY KEY (coorte_id, prato_id)
            );
            CREATE TABLE interacao (
                usuario_id INTEGER NOT NULL,
                prato_id INTEGER NOT NULL REFERENCES prato(id),
                nota INTEGER NOT NULL CHECK (nota BETWEEN 1 AND 5),
                tempo_visualizado INTEGER NOT NULL DEFAULT 0,
                split TEXT NOT NULL CHECK (split IN ('treino', 'teste')),
                PRIMARY KEY (usuario_id, prato_id)
            );
            CREATE INDEX interacao_usuario_split
                ON interacao(usuario_id, split);
            """
        )

        pratos_usados = set()
        for coorte_id, grupo in enumerate(coortes, start=1):
            usuario_id = coorte_id
            conexao.execute(
                "INSERT INTO coorte (id, usuario_id) VALUES (?, ?)",
                (coorte_id, usuario_id),
            )
            for prato_id in grupo:
                pratos_usados.add(prato_id)
                conexao.execute(
                    "INSERT OR IGNORE INTO prato (id, ingredient_ids) VALUES (?, ?)",
                    (
                        prato_id,
                        " ".join(map(str, receitas[prato_id])),
                    ),
                )
                conexao.execute(
                    "INSERT INTO coorte_prato (coorte_id, prato_id) VALUES (?, ?)",
                    (coorte_id, prato_id),
                )

            for prato_id in grupo[:INTERACOES_TREINO]:
                conexao.execute(
                    """
                    INSERT INTO interacao
                        (usuario_id, prato_id, nota, tempo_visualizado, split)
                    VALUES (?, ?, 5, 0, 'treino')
                    """,
                    (usuario_id, prato_id),
                )

            conexao.execute(
                """
                INSERT INTO interacao
                    (usuario_id, prato_id, nota, tempo_visualizado, split)
                VALUES (?, ?, 5, 0, 'teste')
                """,
                (usuario_id, grupo[INTERACOES_TREINO]),
            )

    print(
        f"Base demonstrativa criada em {BANCO_METRICAS} "
        f"({len(coortes)} usuários, {len(pratos_usados)} receitas)."
    )


if __name__ == "__main__":
    criar_banco()
