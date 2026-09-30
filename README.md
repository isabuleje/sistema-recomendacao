# 🍽️ PratoMatch — Sistema de Recomendação de Pratos Culinários

Sistema de recomendação de **pratos culinários**, desenvolvido para sugerir receitas personalizadas de acordo com o histórico e as preferências dos usuários.

O sistema utiliza:

1. **[MÉTODO DE RECOMENDAÇÃO]** para identificar usuários/pratos relacionados e gerar recomendações personalizadas.
2. **[SEGUNDO MÉTODO]** para considerar as alergias e estilos de vida do usuário.

As técnicas são combinadas em um sistema **[HÍBRIDO ]**.

A interface foi desenvolvida utilizando **React **, enquanto o backend utiliza **Django**.

> 🎥 **Vídeo de demonstração:** [ADICIONAR LINK AQUI]

---

## 1. Objetivo

O objetivo do PratoMatch é **recomendar pratos culinários personalizados aos usuários**, considerando suas interações anteriores e suas preferências alimentares.

O sistema deve:

- utilizar uma **base de interações usuário × item**, neste projeto representada por **usuário × prato**;
- aplicar **filtragem colaborativa** para gerar recomendações;
- evitar recomendar pratos que o usuário já avaliou/interagiu;
- permitir consultar o **histórico de pratos avaliados** pelo usuário;
- apresentar uma lista de **pratos recomendados**;
- permitir que o usuário **avalie os pratos**;
- considerar informações como **categorias, ingredientes, tempo de preparo e avaliação média**;
- funcionar também para usuários **sem histórico**, utilizando **On Boarding**;
- ser avaliado utilizando **[NÚMERO] usuários de teste** e **[MÉTODO DE AVALIAÇÃO]**.

---

## 2. Fundamentação

| **Conceito**                 | **Neste projeto**                                                                                                 |
| ---------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| **Filtragem colaborativa**   | [EXPLICAR COMO A FILTRAGEM COLABORATIVA É UTILIZADA]                                                              |
| **Interação usuário × item** | A interação representa a relação entre um **usuário** e um **prato**, registrada por meio de avaliações de 1 a 5. |
| **[ALGORITMO ]**             | [EXPLICAR O ALGORITMO UTILIZADO]                                                                                  |
| **Conteúdo dos pratos**      | [EXPLICAR COMO INGREDIENTES, CATEGORIAS, TEMPO ETC. SÃO UTILIZADOS]                                               |
| **Sistema híbrido**          | [EXPLICAR, CASO O SISTEMA COMBINE MAIS DE UMA TÉCNICA]                                                            |
| **Cold start**               | [EXPLICAR O QUE ACONTECE QUANDO O USUÁRIO NÃO POSSUI HISTÓRICO]                                                   |
| **Personalização**           | [EXPLICAR COMO AS RECOMENDAÇÕES SÃO PERSONALIZADAS]                                                               |

### 2.1 Filtragem colaborativa

[EXPLICAR AQUI, COM SUAS PALAVRAS, COMO O MÉTODO FUNCIONA NO PROJETO.]

Exemplo:

> Usuários que possuem avaliações/interações semelhantes podem ser utilizados para encontrar pratos que um determinado usuário ainda não avaliou.

## 3. Dados

### 3.1 Fontes utilizadas

| **Dataset / Fonte**      | **Conteúdo**                                                               | **Uso no projeto**                 |
| ------------------------ | -------------------------------------------------------------------------- | ---------------------------------- |
| **RAW_recipes.csv**      | Informações das receitas, como nome, ingredientes, tags, tempo e descrição | Cadastro/informações dos pratos    |
| **RAW_interactions.csv** | Interações entre usuários e receitas                                       | Filtragem colaborativa / histórico |
| **PP_recipes.csv**       | [DESCREVER]                                                                | [DESCREVER]                        |
| **INGR_MAP.PKL**         | Ingredientes                                                               | Alergias                           |

**Link das fontes:** (https://www.kaggle.com/datasets/shuyangli94/food-com-recipes-and-user-interactions)

### 3.2 Características dos dados

- Número total de receitas: **[NÚMERO]**
- Número total de usuários utilizados: **[NÚMERO]**
- Número total de interações: **[NÚMERO]**
- Número de categorias: **[NÚMERO]**
- Número de ingredientes: **[NÚMERO]**
- Período dos dados: **[PERÍODO]**

### 3.3 Preparação dos dados

Os dados passam pelas seguintes etapas:

1. **Carregamento dos datasets:** [DESCREVER].
2. **Limpeza dos dados:** Os dados passaram por um tipo de limpeza onde alguns conteúdos que não se adequavam no sistema foram retirados
3. **Tratamento de valores ausentes:** [DESCREVER].
4. **Conversão de listas/categorias:** [DESCREVER].
5. **Relacionamento entre receitas e interações:** [DESCREVER].
6. **Criação dos dados utilizados pelo recomendador:** [DESCREVER].

---

## 4. Método

### 4.1 Preparação para recomendação

[DESCREVER O FLUXO COMPLETO.]

Exemplo:

```text
Dados das receitas
       ↓
Limpeza e preparação
       ↓
Dados de usuários e interações
       ↓
Construção da matriz usuário × prato
       ↓
Algoritmo de recomendação
       ↓
Remoção dos pratos já avaliados
       ↓
Ranking de recomendações
       ↓
Interface do PratoMatch
```

### 4.2 Algoritmo de recomendação

**Algoritmo utilizado:** [NOME]

[EXPLICAR AQUI COMO O ALGORITMO GERA AS RECOMENDAÇÕES.]

Parâmetros principais:

| Parâmetro   |   Valor | Descrição   |
| ----------- | ------: | ----------- |
| [PARÂMETRO] | [VALOR] | [DESCRIÇÃO] |
| [PARÂMETRO] | [VALOR] | [DESCRIÇÃO] |
| [PARÂMETRO] | [VALOR] | [DESCRIÇÃO] |

### 4.3 Tratamento dos pratos já conhecidos

Para evitar recomendações repetidas:

[EXPLICAR COMO OS PRATOS QUE O USUÁRIO JÁ AVALIOU/INTERAGIU SÃO REMOVIDOS.]

### 4.4 Cold start

Para usuários que ainda não possuem histórico:

[EXPLICAR A SOLUÇÃO UTILIZADA.]

Possibilidades utilizadas no projeto:

- [ ] pratos mais populares;
- [ ] pratos com maior avaliação média;
- [ ] preferências selecionadas no cadastro;
- [ ] categorias escolhidas pelo usuário;
- [ ] recomendações por conteúdo;
- [ ] outra: **[DESCREVER]**.

### 4.5 Fluxo do usuário

1. Usuário realiza cadastro/login.
2. Usuário informa **[PREFERÊNCIAS / CATEGORIAS / OUTRAS INFORMAÇÕES]**.
3. Sistema apresenta **[PRATOS INICIAIS / RECOMENDAÇÕES]**.
4. Usuário visualiza os pratos.
5. Usuário avalia os pratos.
6. As interações são armazenadas no banco de dados.
7. O sistema utiliza essas informações para gerar novas recomendações.

---

## 5. Avaliação

### 5.1 Protocolo de avaliação

[EXPLICAR COMO O SISTEMA FOI TESTADO.]

- Quantidade de usuários de teste: **[NÚMERO]**
- Quantidade de pratos utilizados: **[NÚMERO]**
- Quantidade de interações: **[NÚMERO]**
- Divisão entre treinamento e teste: **[DESCREVER]**
- Quantidade de recomendações avaliadas por usuário: **[NÚMERO]**

### 5.2 Métricas

O sistema foi avaliado utilizando as seguintes métricas:

| **Métrica**     | **Descrição**                                                                             |
| --------------- | ----------------------------------------------------------------------------------------- |
| **Precision@K** | [DESCREVER]                                                                               |
| **Recall@K**    | [DESCREVER]                                                                               |
| **NDCG@K**      | [DESCREVER, SE UTILIZADA]                                                                 |
| **HitRate@K**   | [DESCREVER, SE UTILIZADA]                                                                 |
| **MRR@5**       | Média do inverso da posição do primeiro item relevante nas cinco primeiras recomendações. |


### 5.3 Exemplos de usuários

| **Usuário** | **Histórico** | **Recomendações** | **Resultado** |
| ----------- | ------------- | ----------------- | ------------- |
| [USUÁRIO 1] | [PRATOS]      | [PRATOS]          | [RESULTADO]   |
| [USUÁRIO 2] | [PRATOS]      | [PRATOS]          | [RESULTADO]   |
| [USUÁRIO 3] | [PRATOS]      | [PRATOS]          | [RESULTADO]   |
| [USUÁRIO 4] | [PRATOS]      | [PRATOS]          | [RESULTADO]   |
| [USUÁRIO 5] | [PRATOS]      | [PRATOS]          | [RESULTADO]   |

---

## 6. Resultados

### 6.1 Resultados gerais

[APRESENTAR OS RESULTADOS OBTIDOS.]

| **Método**     | **Precision@K** | **Recall@K** | **NDCG@K** | **HitRate@K** |
| -------------- | --------------: | -----------: | ---------: | ------------: |
| [BASELINE]     |         [VALOR] |      [VALOR] |    [VALOR] |       [VALOR] |
| [MÉTODO 1]     |         [VALOR] |      [VALOR] |    [VALOR] |       [VALOR] |
| [MÉTODO 2]     |         [VALOR] |      [VALOR] |    [VALOR] |       [VALOR] |
| [MÉTODO FINAL] |         [VALOR] |      [VALOR] |    [VALOR] |       [VALOR] |

### 6.2 Exemplos de recomendações

**Usuário:** [NOME/ID]

**Histórico:**

- [PRATO]
- [PRATO]
- [PRATO]

**Recomendações:**

1. [PRATO]
2. [PRATO]
3. [PRATO]
4. [PRATO]
5. [PRATO]

**Explicação:** [EXPLICAR POR QUE ESSAS RECEITAS FORAM RECOMENDADAS.]

### 6.3 Usuário sem histórico

**Usuário:** [ID]

**Histórico:** Nenhum.

**Recomendações apresentadas:**

1. [PRATO]
2. [PRATO]
3. [PRATO]
4. [PRATO]
5. [PRATO]

**Método utilizado para o cold start:** [DESCREVER]

---

## 7. Interface

O PratoMatch possui uma interface desenvolvida em **React**.

### 7.1 Página inicial

A página inicial apresenta:

- Pratos recomendados;
- Barra de pesquisa
- Filtro

### 7.2 Favoritos

A página de histórico permite ao usuário visualizar:

- Pratos favoritados

### 7.3 Avaliados

A página de favorito permite ao usuário visualizar:

- Pratos avaliados e a respectiva nota

### 7.3 Detalhes da receita

A tela de recomendações apresenta:

- Nome do prato;
- Imagem;
- Descrição;
- Categorias;
- Tempo de preparo;
- Quantidade de avaliações;
- Avaliação média;
- Número de passos;
- Passos detalhados;
- Opção de avaliar prato;

### 7.4 Filtros

Os filtros disponíveis são:

- Vegetariano;
- Vegano;
- Sem glúten;
- Sem lactose;

### 7.5 Cadastro e Login

Durante o cadastro e login, o usuário pode informar:

- Nome
- Senha

### 7.6 On Boarding

No On Boarding, logo depois do cadastro, possui:

- Etapa 1: Selecionar alergias e estilo de vida (vegatariano, vegano, sem lactose, etc..)
- Etapa 2: Selecionar categorias preferidas
- Etapa 3: Selecionar pratos que o usuário possua interesse

### 7.7 Perfil do usuário

Interface que disponibiliza acesso:

- Mudar/ Visualizar alergias
- Mudar/Visualizar preferências
- Mudar senha
- Excluir conta

### 7.8 Imagens da interface

**Tela inicial**

[INSERIR IMAGEM]

**Tela de recomendações**

[INSERIR IMAGEM]

**Tela de histórico**

[INSERIR IMAGEM]

**Tela de cadastro/onboarding**

[INSERIR IMAGEM]

---

## 8. Limitações

- [LIMITAÇÃO 1]
- [LIMITAÇÃO 2]
- [LIMITAÇÃO 3]
- [LIMITAÇÃO 4]
- [LIMITAÇÃO 5]

### Trabalhos futuros

- [MELHORIA 1]
- [MELHORIA 2]
- [MELHORIA 3]
- [MELHORIA 4]
- [MELHORIA 5]

---

## 9. Como executar

### Requisitos

- Python **3.14.7**
- Node.js **v24.21.0**
- npm **11.19.0**

### Comando para executar

O seguinte comando inicia Venv e ativa o backend e frontend:

```bash
python iniciar_pratomatch.py
```

Backend disponível em:

```text
http://127.0.0.1:8000
```

### Frontend

```text
http://localhost:[PORTA]
```

### Execução do sistema de recomendação

[DESCREVER AQUI SE EXISTIR UM SCRIPT ESPECÍFICO PARA TREINAR/EXECUTAR O RECOMENDADOR.]

```bash
[COMANDO]
```

---

## 10. Estrutura do projeto

```

 backend/
  ├── dataset/
  │   ├── RAW_recipes.csv
  │   ├── RAW_interactions.csv
  │   └── PP_recipes.csv
  │
  ├── PratoMatch/
  │   ├── manage.py
  │   ├── configs/
  │   └── myapp/
      └── db.sqlite3
  │
  ├── recomendacao/
  │   └── main.py
      └── algoritmos.py
  │
  └── requirements.txt
  frontend/
  └── PratoMatch/
     ├── src/
       ├── assets/
       ├── components/
       ├── hooks/
       ├── layouts/
       ├── pages/
       ├── services/
       ├── public/
       ├── package.json
       └── App.jsx
  README.md
  .gitignore
  inciar_pratmatch.py
```

---

## 11. Referências

- [REFERÊNCIA SOBRE FILTRAGEM COLABORATIVA]
- [REFERÊNCIA SOBRE SISTEMAS DE RECOMENDAÇÃO]
- [REFERÊNCIA SOBRE O DATASET]
- [REFERÊNCIA SOBRE O ALGORITMO UTILIZADO]
- [OUTRAS REFERÊNCIAS]

---

## 12. Equipe

| Nome    | Função       |
| ------- | ------------ |
| Isabela | Full-Stack   |
| João    | Recomendação |

**Instituição:** UEA - Universidade Estadual do Amazonas

**Curso:** Sistemas de Informação

**Disciplina:** Oficina de Desenvolvimento de Sistema 1

**Professor(a):** Fábio

**Data:** 30/09/2026
