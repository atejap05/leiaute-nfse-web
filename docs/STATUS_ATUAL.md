# Status Atual do Projeto

Data de referencia: 19 de fevereiro de 2026

## 1. Visao Geral

O projeto esta funcional para uso local de consulta NFSe, com backend e frontend ativos e integrados por HTTP.

Resumo:

- API implementada com foco em leitura e comparacao de dados
- Frontend com paginas principais de busca, regras, cenarios e detalhe de servico
- Banco SQLite populado com dados de referencia
- Base pronta para consolidacao de qualidade (testes automatizados e CI/CD)

## 2. Arquitetura

### Backend (`leiaute-nfse-api`)

Stack:

- FastAPI 0.104.1
- SQLAlchemy 2.0.23
- Pydantic 2.5.0
- SQLite

Modulos principais:

- `app/main.py`: bootstrap da aplicacao, CORS, middleware de log, handlers globais
- `app/config.py`: configuracao via ambiente
- `app/database.py`: engine, sessao e inicializacao de banco
- `app/models.py`: modelos ORM + schemas de resposta
- `app/routers/*`: dominios da API

Rotas implementadas:

- Servicos: 3
- Regras: 4
- Cenarios: 5
- Busca: 3
- Infra/health: 2 (`/health`, `/`)

Total HTTP endpoints: 17
Total endpoints de negocio (`/api/*`): 15

### Frontend (`leiaute-nfse-ui`)

Stack:

- React 18
- TypeScript 5
- Vite 5
- TailwindCSS
- Axios

Modulos principais:

- `src/pages/SearchPage.tsx`
- `src/pages/RulesPage.tsx`
- `src/pages/ScenariosPage.tsx`
- `src/pages/ServiceDetailPage.tsx`
- `src/services/api.ts`

## 3. Dados

Banco: `leiaute-nfse-api/nfse_leiaute.db`

Contagem atual:

- `servicos`: 328
- `regras`: 677
- `cenarios`: 112
- `campos_layout`: 431
- `restricoes`: 0
- `master_index`: 1

Total registros principais: 1.549

## 4. Estado Funcional

### Concluido

- API principal implementada
- Busca unificada em servicos/regras/campos
- Modelos de resposta tipados na maior parte das rotas
- CORS configuravel por ambiente
- Handlers globais de erro padronizados
- Logging estruturado por request com `request_id`
- Normalizacao de resposta de busca no frontend

### Em progresso

- Padronizacao completa de `response_model` nas rotas de busca auxiliares
- Suite automatizada de testes em pipeline

### Nao iniciado

- CI/CD (GitHub Actions)
- autenticacao/autorizacao
- rate limiting
- observabilidade externa (metrics/traces)

## 5. Qualidade e Operacao

Situacao atual:

- Testes backend existem em `leiaute-nfse-api/tests/test_api.py`
- Pipeline automatico ainda nao configurado
- Build frontend possui pendencia de configuracao TS em `vite.config.ts` (`path`/`__dirname`)

## 6. Objetivos da Proxima Sprint

1. Fechar baseline de engenharia

- corrigir build TypeScript no frontend
- configurar pytest + coverage no backend
- adicionar workflow CI minimo

2. Melhorar robustez da API

- remover `response_model=dict` remanescente
- padronizar contratos de erro em todas as rotas

3. Preparar ambiente de deploy

- guias de execucao por ambiente
- checklist de release

## 7. Indicadores de Prontidao (MVP Tecnico)

- API funcional local: concluido
- Frontend integrado local: concluido
- Testes automatizados em CI: nao concluido
- Build e lint sem erro: nao concluido
- Seguranca de acesso: nao concluido

Status geral: MVP tecnico parcialmente pronto, com foco imediato em qualidade operacional.
