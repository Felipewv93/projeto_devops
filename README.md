# Projeto DevOps: Dashboard de Filmes

Este projeto é uma aplicação completa para análise de dados de bilheteria de filmes, composta por três serviços principais: banco de dados PostgreSQL, API em FastAPI e dashboard interativo em Streamlit. O ambiente é totalmente orquestrado com Docker Compose.

## Visão Geral

- **Banco de Dados (PostgreSQL):** Armazena informações de filmes, incluindo título, diretor, estúdio, gênero, ano de lançamento e bilheteria. Inicializado com dados reais de grandes bilheterias.
- **API (FastAPI):** Fornece endpoints REST para consulta, análise e inserção de filmes. Utiliza SQLAlchemy para ORM e Pydantic para validação.
- **Dashboard (Streamlit):** Interface web interativa para visualização de análises, gráficos e inserção de novos filmes, consumindo dados da API.

## Estrutura do Projeto

```
docker-compose.yml
init.sql
api/
  Dockerfile
  main.py
  requirements.txt
dashboard/
  app.py
  Dockerfile
  requirements.txt
```

## Como Executar

1. **Pré-requisitos:**
   - Docker e Docker Compose instalados.

2. **Suba os serviços:**
   ```sh
   docker-compose up --build
   ```
   Isso irá:
   - Criar o banco de dados e popular com dados iniciais (via `init.sql`)
   - Subir a API em FastAPI na porta 8000
   - Subir o dashboard Streamlit na porta 8501

3. **Acesse:**
   - Dashboard: [http://localhost:8501](http://localhost:8501)
   - API (Swagger): [http://localhost:8000/docs](http://localhost:8000/docs)
   - Banco de Dados: localhost:5432 (usuário: postgres, senha: postgres, banco: filmesdb)

## Funcionalidades

- **Dashboard:**
  - Visualização de gráficos de bilheteria, gêneros e estúdios
  - Inserção de novos filmes
  - Filtros e análises interativas
- **API:**
  - Listagem de filmes
  - Análises por gênero e estúdio
  - Inserção de filmes via POST
- **Banco de Dados:**
  - Estrutura relacional otimizada para consultas analíticas

## Principais Tecnologias

- **Backend:** FastAPI, SQLAlchemy, Pydantic, Uvicorn
- **Frontend:** Streamlit, Plotly
- **Banco de Dados:** PostgreSQL
- **DevOps:** Docker, Docker Compose

## Instalação Manual (opcional)

Se preferir rodar localmente sem Docker:

1. Suba um PostgreSQL local e execute o `init.sql`.
2. Instale dependências da API:
   ```sh
   pip install -r api/requirements.txt
   ```
3. Instale dependências do dashboard:
   ```sh
   pip install -r dashboard/requirements.txt
   ```
4. Exporte as variáveis de ambiente necessárias e execute os serviços manualmente.

## Créditos e Dados

- Dados de filmes extraídos de fontes públicas de bilheteria.
- Projeto para fins educacionais e demonstração de práticas DevOps.

---

Sinta-se à vontade para contribuir ou adaptar para outros domínios!
