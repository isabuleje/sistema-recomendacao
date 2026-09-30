# 🍽️ PratoMatch — Sistema de Recomendação de Pratos Culinários

Sistema de recomendação de pratos culinários que combina o histórico de avaliações do usuário com suas preferências alimentares, categorias de interesse e alergias.

A aplicação é formada por:

- **Frontend:** React 19, React Router e Vite.
- **Backend:** Django 6.1 e Django REST Framework.
- **Banco de dados:** SQLite, usado pelo Django.
- **Recomendador:** filtragem colaborativa por similaridade de cosseno e k-NN.

> 🎥 **Vídeo de demonstração:** [ADICIONAR LINK AQUI]

---

## 1. Objetivo

O PratoMatch recomenda receitas personalizadas com base nas avaliações dos usuários e em suas preferências alimentares.

O sistema permite:

- cadastrar e autenticar usuários;
- consultar, pesquisar e filtrar pratos;
- visualizar detalhes, ingredientes, categorias e modo de preparo;
- avaliar pratos com notas de 1 a 5;
- favoritar pratos;
- consultar pratos avaliados e favoritados;
- configurar alergias, preferências alimentares e categorias de interesse;
- gerar recomendações personalizadas;
- recomendar pratos a usuários com pouco ou nenhum histórico usando os dados do onboarding.

---

## 2. Fundamentação

| **Conceito**                 | **Neste projeto**                                                                                       |
| ---------------------------- | -------------------------------------------------------------------------------------------------------- |
| **Filtragem colaborativa**   | Usuários são comparados pelas notas dadas aos mesmos pratos.                                             |
| **Interação usuário × item** | Cada interação relaciona um usuário a um prato e registra uma nota de 1 a 5.                              |
| **Similaridade de cosseno**  | Mede a semelhança entre os vetores de avaliações de dois usuários.                                       |
| **k-NN**                     | Seleciona os usuários mais semelhantes para gerar candidatos a recomendação.                             |
| **Conteúdo dos pratos**      | Ingredientes, categorias, tempo, passos e avaliações são usados para exibir e filtrar as receitas.      |
| **Sistema híbrido**          | A recomendação usa filtragem colaborativa e filtros de alergias/preferências do perfil.                  |
| **Cold start**               | O onboarding fornece pratos de interesse até que o usuário tenha histórico suficiente de avaliações.   |
| **Personalização**           | Pratos já avaliados são removidos e os candidatos são filtrados conforme as alergias cadastradas.       |

### 2.1 Filtragem colaborativa

O sistema compara as avaliações dos usuários considerando apenas os pratos em comum. A similaridade de cosseno é calculada quando existem pelo menos três pratos avaliados em comum. Os vizinhos mais semelhantes influenciam a nota prevista dos pratos que o usuário ainda não avaliou.

O ranking final combina a nota prevista com a frequência com que um prato aparece entre os vizinhos. Em seguida, os pratos já avaliados e os que contêm ingredientes associados às alergias do usuário são removidos.

---

## 3. Dados

### 3.1 Fontes utilizadas

| **Dataset / Fonte**      | **Conteúdo**                                                               | **Uso no projeto**                 |
| ------------------------ | -------------------------------------------------------------------------- | ---------------------------------- |
| **RAW_recipes.csv**      | Nome, descrição, ingredientes, tags, tempo e passos das receitas           | Catálogo e detalhes dos pratos     |
| **RAW_interactions.csv** | Usuários, receitas, notas e datas das interações                           | Histórico e filtragem colaborativa |
| **PP_recipes.csv**       | Dados pré-processados das receitas                                         | Dataset auxiliar                   |
| **PP_users.csv**         | Dados pré-processados dos usuários                                         | Dataset auxiliar                   |
| **ingr_map.pkl**         | Mapeamento de ingredientes                                                  | Tratamento de alergias              |
| **interactions_*.csv**   | Divisões de treino, validação e teste                                       | Avaliação offline                  |

**Link da fonte principal:** <https://www.kaggle.com/datasets/shuyangli94/food-com-recipes-and-user-interactions>

### 3.2 Características dos dados

Os arquivos locais atualmente contêm:

- `RAW_recipes.csv`: **231.637** receitas;
- `RAW_interactions.csv`: **1.132.367** interações originais;
- `PP_recipes.csv`: **178.265** registros;
- `PP_users.csv`: **25.076** registros;
- `interactions_train.csv`: **698.901** registros;
- `interactions_validation.csv`: **7.023** registros;
- `interactions_test.csv`: **12.455** registros.

Os arquivos brutos são carregados diretamente pelo módulo de recomendação. Os arquivos de treino, validação e teste ficam disponíveis para avaliações offline.

### 3.3 Preparação dos dados

1. Os CSVs de receitas e interações são carregados com pandas.
2. Campos de tags, ingredientes e passos são convertidos de texto para listas.
3. As tags técnicas são removidas da lista de categorias exibida no sistema.
4. As avaliações são agrupadas por receita para calcular a média e a quantidade de avaliações.
5. Receitas e interações são relacionadas pelos IDs originais.
6. O script `backend/seed.py` popula o banco Django com categorias, pratos, usuários, interações e catálogos de alergias e preferências.

---

## 4. Método

### 4.1 Preparação para recomendação

```text
Dados das receitas e interações
              ↓
Limpeza e conversão dos campos
              ↓
Histórico de avaliações por usuário
              ↓
Similaridade de cosseno entre usuários
              ↓
Seleção dos vizinhos (k-NN)
              ↓
Ranking por nota prevista e frequência
              ↓
Filtros de alergias e pratos já conhecidos
              ↓
Recomendações exibidas no frontend
```

### 4.2 Algoritmo de recomendação

**Algoritmo utilizado:** filtragem colaborativa baseada em usuários, com similaridade de cosseno e k-NN.

Para cada usuário, o sistema:

1. encontra usuários com avaliações semelhantes;
2. seleciona os vizinhos mais próximos;
3. coleta pratos avaliados pelos vizinhos e ainda não avaliados pelo usuário;
4. calcula uma nota prevista ponderada pela influência dos vizinhos;
5. considera a frequência de aparição dos pratos;
6. remove pratos incompatíveis com alergias e pratos já conhecidos;
7. retorna o ranking final.

Parâmetros principais:

| Parâmetro | Valor padrão | Descrição |
| --------- | ------------ | --------- |
| `k` | `1` na chamada da API | Quantidade de vizinhos usados na recomendação |
| `limite` | `60` | Quantidade máxima de recomendações retornadas |
| `minimo_de_avaliacoes_pro_mesmo_prato_pra_nao_desconsiderar` | `3` | Avaliações em comum mínimas para calcular similaridade |
| `valorizacao_de_frequencia` | `0.2` | Peso adicional para pratos recorrentes entre os vizinhos |

### 4.3 Tratamento dos pratos já conhecidos

Os pratos que já aparecem no histórico de interações do usuário não entram no conjunto de recomendações.

### 4.4 Cold start

Quando o usuário possui menos de cinco pratos avaliados, os pratos selecionados como interessados no onboarding são usados como informação inicial do perfil. As preferências e alergias cadastradas também são aplicadas durante a filtragem.

### 4.5 Fluxo do usuário

1. O usuário realiza cadastro ou login.
2. No onboarding, seleciona preferências alimentares, alergias, categorias e pratos de interesse.
3. O sistema apresenta os pratos e recomendações.
4. O usuário pode pesquisar, filtrar, favoritar e avaliar pratos.
5. As avaliações são armazenadas no banco de dados.
6. Novas recomendações são geradas a partir do histórico atualizado.

---

## 5. Avaliação

### 5.1 Protocolo de avaliação

O projeto possui rotinas de avaliação offline em `backend/recomendacao/metricas.py` e `backend/recomendacao/algoritmos.py`.

As divisões disponíveis são:

- `interactions_train.csv`;
- `interactions_validation.csv`;
- `interactions_test.csv`.

O módulo de métricas implementa `MRR@K` e a criação de ground truth a partir de interações com nota mínima. Os valores finais de avaliação devem ser preenchidos após a execução do experimento definido para o projeto.

### 5.2 Métricas

| **Métrica** | **Descrição** |
| ----------- | -------------- |
| **MRR@K** | Média do inverso da posição do primeiro item relevante nas primeiras `K` recomendações. |
| **Ground truth por nota** | Considera relevantes as interações com nota maior ou igual ao limite configurado, que por padrão é 4. |

### 5.3 Exemplos de usuários

Os exemplos e resultados numéricos devem ser adicionados após a execução da avaliação experimental.

---

## 6. Resultados

Os resultados quantitativos ainda não estão registrados neste README. Eles devem ser adicionados após a execução das rotinas de avaliação com os arquivos de treino, validação e teste.

---

## 7. Interface

O PratoMatch possui uma interface desenvolvida em React.

### 7.1 Página inicial

- Lista de pratos;
- recomendações;
- busca por nome;
- filtros alimentares.

### 7.2 Favoritos e avaliados

O usuário pode consultar os pratos favoritados e os pratos avaliados, incluindo sua nota.

### 7.3 Detalhes da receita

A tela de detalhes apresenta:

- nome, imagem e descrição;
- categorias e ingredientes;
- tempo de preparo;
- avaliação média e quantidade de avaliações;
- quantidade e descrição dos passos;
- opção de avaliar e favoritar.

### 7.4 Filtros

- Vegetariano;
- Vegano;
- Sem glúten;
- Sem lactose.

### 7.5 Cadastro e login

O cadastro utiliza nome de usuário e senha.

### 7.6 Onboarding

O onboarding possui três etapas:

1. seleção de alergias e preferências alimentares;
2. seleção de categorias preferidas;
3. seleção de pratos de interesse.

### 7.7 Perfil do usuário

O perfil permite visualizar e alterar preferências e alergias, alterar a senha e excluir a conta.

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

- O recomendador depende de usuários com avaliações em comum.
- A recomendação é baseada principalmente em avaliações, e não em um modelo treinado de conteúdo.
- O tratamento de alergias depende do mapeamento disponível em `ingr_map.pkl`.
- Os resultados experimentais ainda precisam ser documentados.
- O banco SQLite é adequado para desenvolvimento, mas não é a opção indicada para produção.

### Trabalhos futuros

- executar e documentar a avaliação offline;
- comparar o método atual com baselines;
- melhorar a recomendação baseada no conteúdo das receitas;
- adicionar paginação e cache para recomendações;
- preparar o sistema para implantação em produção.

---

## 9. Como executar

### Requisitos

- Python 3.14.7;
- Node.js v24.21.0;
- npm 11.19.0.

As versões das bibliotecas Python estão fixadas em `backend/requirements.txt`. As dependências do frontend estão em `frontend/PratoMatch/package.json`.

### Comando para executar

Na raiz do projeto:

```bash
python iniciar_pratomatch.py
```

O script cria ou reutiliza o ambiente virtual em `backend/venv`, instala as dependências e inicia o backend e o frontend.

Backend disponível em:

```text
http://127.0.0.1:8000
```

Frontend:

```text
http://localhost:5173
```

A porta exibida pelo Vite deve ser usada caso a porta padrão esteja ocupada.

### Popular o banco

Para aplicar as migrações e carregar os dados no banco:

```bash
cd backend
python seed.py
```

Para remover os dados criados pelo seed e carregá-los novamente:

```bash
python seed.py --limpar
```

---

## 10. Estrutura do projeto

```text
backend/
├── dataset/
├── PratoMatch/
│   ├── manage.py
│   ├── configs/
│   └── myapp/
├── recomendacao/
│   ├── algoritmos.py
│   ├── main.py
│   └── metricas.py
├── requirements.txt
└── seed.py

frontend/
└── PratoMatch/
    ├── src/
    │   ├── components/
    │   ├── hooks/
    │   ├── layouts/
    │   ├── pages/
    │   └── services/
    ├── public/
    ├── package.json
    └── vite.config.js

README.md
└── iniciar_pratomatch.py
```

---

## 11. Referências

- [Dataset Food.com Recipes and User Interactions](https://www.kaggle.com/datasets/shuyangli94/food-com-recipes-and-user-interactions)
- [Documentação do Django](https://docs.djangoproject.com/)
- [Documentação do Django REST Framework](https://www.django-rest-framework.org/)
- [Documentação do React](https://react.dev/)
- [Documentação do Vite](https://vite.dev/)

---

## 12. Equipe

| Nome | Função |
| ---- | ------ |
| Isabela | Full-Stack |
| João | Recomendação |

**Instituição:** UEA - Universidade Estadual do Amazonas
**Curso:** Sistemas de Informação
**Disciplina:** Oficina de Desenvolvimento de Sistema 1
**Professor:** Fábio
**Data:** 30/09/2026
