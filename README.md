# SQL Query Optimizer Assistant

Ferramenta que analisa queries SQL e identifica padroes que prejudicam performance, cruzando analise estatica com o plano de execucao real (`EXPLAIN ANALYZE`) do PostgreSQL.

Projeto de portfolio para demonstrar conhecimento pratico em SQL, banco de dados relacional e Python, com foco em diagnostico de performance de queries (e nao apenas em um CRUD comum).

## Como funciona

1. Voce cola uma query SQL (ou carrega um dos exemplos prontos).
2. O `analyzer` aplica um conjunto de regras estaticas sobre o texto da query, identificando antipadroes comuns.
3. A aplicacao roda `EXPLAIN (FORMAT JSON, ANALYZE)` no PostgreSQL real e identifica os nos de `Seq Scan` no plano, mostrando custo e tempo de execucao reais.
4. Tudo e exibido em uma interface Streamlit.

## Regras de analise estatica implementadas

| Regra | Severidade | Problema |
|---|---|---|
| SELECT_STAR | MEDIA | `SELECT *` traz colunas desnecessarias |
| MISSING_WHERE | MEDIA | Falta de `WHERE` forca leitura completa da tabela |
| LEADING_WILDCARD_LIKE | ALTA | `LIKE '%termo'` impede uso de indice B-tree |
| FUNCTION_ON_COLUMN | ALTA | Funcao sobre coluna no `WHERE` (ex: `UPPER(coluna)`) impede uso de indice |
| OR_IN_WHERE | BAIXA | `OR` no `WHERE` pode reduzir eficiencia de indices compostos |

## Exemplo real

Rodando `examples/query_03.sql` (`WHERE UPPER(cd_cpf) = '...'`) contra a tabela `pessoa_fisica` com 500.000 registros:

- A analise estatica aponta `FUNCTION_ON_COLUMN` (severidade ALTA).
- O plano de execucao real confirma: a tabela tem um indice em `cd_cpf` (`idx_pessoa_cpf`), mas o `UPPER()` o invalida — o Postgres faz **Seq Scan** mesmo a busca nao retornando nenhuma linha, levando ~80ms contra uma tabela que poderia ser resolvida em menos de 1ms com o indice sendo usado.

## Estrutura do projeto

```
sql-query-optimizer-assistant/
├── app.py                   # Interface Streamlit
├── config.py                 # Configuracao via variaveis de ambiente (.env)
├── requirements.txt
├── analyzer/
│   ├── rules.py              # Regras de analise estatica
│   └── sql_analyzer.py       # Orquestra as regras + integracao com EXPLAIN ANALYZE
├── database/
│   ├── connection.py         # Conexao com PostgreSQL (psycopg 3)
│   └── seed.py                # Gera dados sinteticos em massa (Faker) para testes de performance
├── examples/                 # Queries de exemplo, cada uma ilustrando um problema diferente
└── tests/
    └── test_rules.py         # Testes unitarios das regras
```

## Banco de dados utilizado nos testes

Schema `performance_tests` com as tabelas `pessoa_fisica`, `pessoa_fisica_email`, `pessoa_fisica_telefone` e `pessoa_fisica_endereco`, populadas com **500.000+ registros sinteticos** (gerados via `database/seed.py` com Faker). O volume real permite observar diferencas concretas entre planos de execucao (Seq Scan vs Index Scan) — com poucas linhas o planner do Postgres nunca usa indice, pois nao compensa.

## Como executar localmente

### 1. Pre-requisitos

- Python 3.11+
- PostgreSQL rodando localmente (ou acessivel via rede)

### 2. Configuracao

```bash
git clone <url-do-repositorio>
cd sql-query-optimizer-assistant
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux/Mac
pip install -r requirements.txt
cp .env.example .env           # edite com suas credenciais de banco
```

### 3. Popular o banco com dados de teste (opcional, mas recomendado)

```bash
python -m database.seed --count 500000
```

### 4. Rodar os testes

```bash
pytest tests/ -v
```

### 5. Rodar a aplicacao

```bash
streamlit run app.py
```

## Tecnologias

- Python 3.13
- PostgreSQL + psycopg 3
- Streamlit
- Faker (geracao de dados sinteticos)
- pytest
