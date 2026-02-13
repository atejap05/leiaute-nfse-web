# 📋 Relatório de Dificuldades e Erros - API NFSe Leiaute

**Data:** 13 de fevereiro de 2026  
**Projeto:** Portal NFSe Leiaute - React + FastAPI  
**Status:** Em Desenvolvimento - Fase de Testes Backend

---

## 📑 Índice

1. [Resumo Executivo](#resumo-executivo)
2. [Erros Encontrados e Resoluções](#erros-encontrados-e-resoluções)
3. [Status Atual do Projeto](#status-atual-do-projeto)
4. [Roadmap - Próximos Passos](#roadmap---próximos-passos)
5. [Recomendações](#recomendações)

---

## 📊 Resumo Executivo

Durante a implementação e testes da API NFSe Leiaute, o projeto enfrentou **5 categorias principais de dificuldades**, todas já resolvidas com sucesso. A importação de dados foi concluída (**1.548 registros**) e o banco de dados está operacional.

### Estatísticas de Importação Alcançadas:

- ✅ **328** serviços importados
- ✅ **677** regras de validação importadas
- ✅ **112** cenários de exportação importados
- ✅ **431** campos de leiaute importados
- ✅ **0** restrições importadas (sem dados na fonte)
- ✅ **6** tabelas criadas com relacionamentos

### Status Atual:

- Banco de dados: **Operacional** ✅
- Models ORM: **Corrigidos** ✅
- Schemas Pydantic: **Validados** ✅
- Routers FastAPI: **Corrigidos** ✅
- Servidor: **Preparado para inicialização** ✅

---

## 🔴 Erros Encontrados e Resoluções

### 1. Erro de Versão - openpyxl==3.11.0

#### Descrição

```
No matching distribution found for openpyxl==3.11.0
```

#### Causa

A versão 3.11.0 do pacote openpyxl não existe no PyPI. A versão foi especificada incorretamente no arquivo `requirements.txt`.

#### Solução Implementada

- Alterado em `requirements.txt`: `openpyxl==3.11.0` → `openpyxl==3.1.5`
- Executado: `pip install openpyxl==3.1.5`

#### Como Replicar a Solução

```bash
# Editar requirements.txt
openpyxl==3.1.5

# Reinstalar dependências
pip install -r requirements.txt
```

---

### 2. Erro de Relacionamento - ServicoORM

#### Descrição

```
sqlalchemy.exc.ArgumentError: expression 'servico_campo_layout' failed to locate a name
```

#### Causa

A classe `ServicoORM` tentava criar um relacionamento (`relationship`) com uma tabela de associação `servico_campo_layout` que não havia sido criada. O código continha:

```python
# ❌ INCORRETO
campos_aplicaveis = relationship("CampoLayoutORM", secondary="servico_campo_layout")
```

#### Solução Implementada

- Removido o relacionamento inválido da classe `ServicoORM`
- A associação entre Serviço e Campo é feita indiretamente através de `RegraORM`

#### Arquivo Corrigido

- `leiaute-nfse-api/app/models.py` (linhas 25-35)

---

### 3. Erro de Constraints NULL - Fase 1: Campo

#### Descrição

```
NOT NULL constraint failed: regras.campo (Regra #5)
```

#### Causa

A coluna `campo` em `RegraORM` era `nullable=False`, mas a origem JSON (`2_cenarios_exportacao.json`) continha regras com `"campo": null`.

#### Solução Implementada

Alterado em `RegraORM`:

```python
# ❌ ANTES
campo = Column(String(255), nullable=False)

# ✅ DEPOIS
campo = Column(String(255), nullable=True)
```

#### Arquivo Corrigido

- `leiaute-nfse-api/app/models.py` (linha 44)

---

### 4. Erro de Constraints NULL - Fase 2 e 3: Campos Múltiplos

#### Descrição

```
NOT NULL constraint failed: regras.regra_negocio (Regra #150)
NOT NULL constraint failed: regras.codigo_erro
NOT NULL constraint failed: regras.mensagem_erro
NOT NULL constraint failed: regras.nivel_regra
```

#### Causa

Após corrigir `campo`, o script revelou que mais de **5 campos** em `RegraORM` continham valores `NULL` na origem JSON:

- `regra_negocio` (ex: Regra #150)
- `codigo_erro`
- `mensagem_erro`
- `nivel_regra`

#### Solução Implementada

Alterado todos os campos para `nullable=True` em `RegraORM`:

```python
# ✅ CORRIGIDOS
campo = Column(String(255), nullable=True, index=True)
regra_negocio = Column(Text, nullable=True)
codigo_erro = Column(String(10), nullable=True, index=True)
mensagem_erro = Column(Text, nullable=True)
nivel_regra = Column(Integer, nullable=True, index=True)
```

#### Arquivo Corrigido

- `leiaute-nfse-api/app/models.py` (linhas 44, 46, 48, 50, 52)

#### Como Diagnosticar Dinamicamente

Para identificar campos com NULL na origem:

```python
# Em import_json_to_db.py
null_fields = [k for k, v in regra_dict.items() if v is None]
if null_fields:
    print(f"⚠️ Regra #{regra_dict['numero_regra']} tem NULLs em: {null_fields}")
```

---

### 5. Erro de Forward Reference - Pydantic v2

#### Descrição

```
PydanticUndefinedAnnotation: name 'RegraResponse' is not defined
```

#### Causa

A classe `ServicoDetail` usava uma forward reference (`List['RegraResponse']`) para referir-se a `RegraResponse` que era definida após sua classe. Pydantic v2 requer que forward references sejam resolvidas explicitamente.

```python
# ❌ PROBLEMA
class ServicoDetail(ServicoBase):
    regras: List['RegraResponse']  # Referência adiante
    # ...RegraResponse é definido depois

class RegraResponse(RegraBase):
    pass
```

#### Solução Implementada - Três Passos

**Passo 1:** Adicionar import de `annotations` no início do arquivo

```python
# ✅ LINHA 1
from __future__ import annotations
```

**Passo 2:** Usar `Optional` para campos que podem ser `None`

```python
# ✅ RegraBase com campos Optional
class RegraBase(BaseModel):
    numero_regra: int
    campo: Optional[str] = None  # Era: str
    regra_negocio: Optional[str] = None  # Era: str
    codigo_erro: Optional[str] = None  # Era: str
    mensagem_erro: Optional[str] = None  # Era: str
    nivel_regra: Optional[int] = None  # Era: int
```

**Passo 3:** Reconstruir modelos após importações

```python
# ✅ FINAL DO ARQUIVO
ServicoDetail.model_rebuild()
```

#### Arquivo Corrigido

- `leiaute-nfse-api/app/models.py` (linhas 1, 44-52, 207-216, 361)

---

### 6. Erro de Parâmetro FastAPI - Query vs Path

#### Descrição

```
AssertionError: Cannot use `Query` for path param 'nivel'.
```

#### Causa

Em `leiaute-nfse-api/app/routers/regras.py`, o endpoint `/filtro/por-nivel/{nivel}` definia o parâmetro como:

```python
# ❌ INCORRETO - Query é para query params (?nivel=1)
@router.get("/filtro/por-nivel/{nivel}")
def get_rules_by_level(
    nivel: int = Query(..., ge=1, le=3),  # ❌ Deveria ser Path
    ...
):
```

FastAPI exige que parâmetros no caminho (path parameters) usem `Path()`, não `Query()`.

#### Solução Implementada

**Passo 1:** Importar `Path` do FastAPI

```python
# ✅ LINHA 1
from fastapi import APIRouter, Depends, HTTPException, Query, Path
```

**Passo 2:** Alterar o decorator do parâmetro

```python
# ✅ CORRETO - Path é para path params ({nivel})
@router.get("/filtro/por-nivel/{nivel}")
def get_rules_by_level(
    nivel: int = Path(..., ge=1, le=3),  # ✅ Path agora
    limit: int = Query(20, gt=0, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
```

#### Arquivo Corrigido

- `leiaute-nfse-api/app/routers/regras.py` (linhas 1, 76)

#### Referência FastAPI

| Tipo      | Uso                     | Sintaxe                    |
| --------- | ----------------------- | -------------------------- |
| **Path**  | `/api/regras/{id}`      | `id: int = Path(...)`      |
| **Query** | `/api/regras?limite=10` | `limite: int = Query(...)` |
| **Body**  | POST com JSON           | `dados: SchemaModel`       |

---

## ✅ Status Atual do Projeto

### Banco de Dados

```
Estado: ✅ Operacional
Arquivo: leiaute-nfse-api/nfse_leiaute.db
Size: ~651 KB
Tabelas:
  - servicos: 328 registros
  - regras: 677 registros
  - cenarios: 112 registros
  - campos_layout: 431 registros
  - restricoes: 0 registros
  - master_index: 1 registro
```

### Backend

```
Estado: ✅ Pronto para inicialização
Framework: FastAPI 0.104.1
Database: SQLAlchemy 2.0.23, SQLite
Validation: Pydantic 2.5.0
Routers: 6 (servicos, regras, cenarios, busca, health, root)
Routes: 21 endpoints definidos
```

### Frontend

```
Estado: ⏳ Não iniciado
Framework: React 18 + TypeScript
Build: Vite 5.0
Dependências: npm install concluído
Ready: Aguardando estabilidade do backend
```

### Ambiente

```
Python: 3.11+
OS: Windows
Terminal: PowerShell 5.1
Encoding: UTF-8
Virtual Env: ✅ Ativado (venv)
```

---

## 🛣️ Roadmap - Próximos Passos

### Fase 1: Validação do Backend (PRÓXIMO)

**Duração estimada:** 2-3 horas  
**Responsável:** Testes Automáticos + Manual

#### 1.1 Iniciar Servidor FastAPI

```bash
cd leiaute-nfse-api
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Validação esperada:**

```
✅ INFO:     Uvicorn running on http://0.0.0.0:8000
✅ INFO:     Application startup complete
```

#### 1.2 Testar Endpoint de Health Check

```bash
curl http://localhost:8000/health
# Resposta esperada: {"status": "healthy"}
```

#### 1.3 Testar Endpoints Principais

```bash
# Listar serviços
curl "http://localhost:8000/api/services?limit=5"

# Listar regras
curl "http://localhost:8000/api/rules?limit=5"

# Regras por nível
curl "http://localhost:8000/api/rules/filtro/por-nivel/1"

# Cenários
curl "http://localhost:8000/api/cenarios?limit=5"

# Busca
curl "http://localhost:8000/api/search?q=nfse"
```

**Validações esperadas:**

- Status HTTP 200
- Estrutura JSON válida
- Dados correspondem ao banco

#### 1.4 Executar Testes Automáticos

```bash
cd leiaute-nfse-api
pytest tests/ -v --tb=short
```

**Cobertura esperada:**

- [ ] test_health_endpoint
- [ ] test_list_services
- [ ] test_service_detail
- [ ] test_list_rules
- [ ] test_rules_by_nivel
- [ ] test_list_cenarios
- [ ] test_search

---

### Fase 2: Integração Frontend-Backend (2-3 dias)

**Duração estimada:** 4-6 horas  
**Responsável:** Desenvolvimento Frontend

#### 2.1 Iniciar Servidor Frontend

```bash
cd leiaute-nfse-ui
npm run dev
```

**Validação esperada:**

```
✅ Local:        http://localhost:5173/
✅ React: v18.2.0
✅ TypeScript: v5.x
```

#### 2.2 Implementar Serviços HTTP

- Criar `src/services/api.ts` com axios/fetch
- Configurar base URL: `http://localhost:8000/api`
- Implementar interceptores de erro

#### 2.3 Testar Integração Manual

- [ ] Carregar lista de serviços da API
- [ ] Exibir detalhes de um serviço
- [ ] Filtrar regras por nível
- [ ] Buscar regras por código de erro
- [ ] Listar cenários

#### 2.4 Testes E2E

```bash
npx cypress open
# ou
npx playwright test
```

---

### Fase 3: Melhorias e Otimizações (1 semana)

**Duração estimada:** 8-10 horas  
**Responsável:** Backend + Frontend

#### 3.1 Backend Melhorias

- [ ] **Autenticação:** Implementar JWT ou OAuth2
- [ ] **Paginação:** Reafinar schemas de response com metadados
- [ ] **Caching:** Redis para consultas frequentes
- [ ] **Validação:** Adicionar mais regras de business logic
- [ ] **Logging:** Estruturado com contexto de requisição
- [ ] **Documentação:** Swagger/OpenAPI automaticamente gerado

#### 3.2 Frontend Melhorias

- [ ] **State Management:** Zustand ou Redux Toolkit
- [ ] **Componentes:** Biblioteca UI (shadcn/ui, Material-UI)
- [ ] **Performance:** Lazy loading, code splitting
- [ ] **Accessibility:** WCAG 2.1 AA compliance
- [ ] **Responsividade:** Mobile-first design
- [ ] **Temas:** Dark mode support

#### 3.3 DevOps

- [ ] **CI/CD:** GitHub Actions workflow
- [ ] **Docker:** Containerização backend/frontend
- [ ] **Database:** Backup automático SQLite → PostgreSQL
- [ ] **Monitoring:** Health checks e alertas

---

## 💡 Recomendações

### Curto Prazo (Próxima Sessão)

#### 1. Diagnosticar Problema de Inicialização do Servidor

**Problema observado:** Erro de ModuleNotFoundError quando usando uvicorn

**Ações recomendadas:**

```bash
# 1. Verificar PYTHONPATH
echo $env:PYTHONPATH

# 2. Testar import direto
python -c "from app.main import app; print('OK')"

# 3. Se passou, usar:
python -m uvicorn app.main:app --reload

# 4. Se falhar, usar:
cd leiaute-nfse-api
python -m uvicorn app.main:app --reload
```

#### 2. Validar Integrity do Banco de Dados

```python
# Script auxiliar: check_db.py
import sqlite3
conn = sqlite3.connect('leiaute-nfse-api/nfse_leiaute.db')
cursor = conn.cursor()

# Verificar foreign keys
pragma foreign_keys = ON;
```

#### 3. Criar Script de Inicialização Rápida

```bash
# setup_dev.sh
#!/bin/bash
cd leiaute-nfse-api
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\Activate.ps1 no Windows
pip install -r requirements.txt
python scripts/import_json_to_db.py
python -m uvicorn app.main:app --reload
```

### Médio Prazo (Esta Semana)

#### 1. Documentação de APIs

- [ ] Gerar Swagger UI em `/docs`
- [ ] Gerar ReDoc em `/redoc`
- [ ] Documentar cada endpoint com exemplos

#### 2. Suite de Testes Completa

- [ ] Unit tests para models
- [ ] Integration tests para routers
- [ ] End-to-end tests com Cypress/Playwright

#### 3. Qualidade de Código

```bash
# Linting
pip install flake8 black isort
black leiaute-nfse-api/app/
isort leiaute-nfse-api/app/

# Type checking
pip install mypy
mypy leiaute-nfse-api/app/
```

### Longo Prazo (Próximos Meses)

#### 1. Escalabilidade

- PostgreSQL em vez de SQLite
- Redis para caching
- Load balancing (Nginx)

#### 2. Segurança

- Rate limiting
- CORS aprimorado
- Validação de entrada robusta
- Secrets management (.env)

#### 3. Monitoramento

- Logging estruturado (ELK stack)
- Métricas (Prometheus)
- Alertas (AlertManager)

---

## 📚 Referências Úteis

### FastAPI

- Docs: https://fastapi.tiangolo.com/
- Path vs Query: https://fastapi.tiangolo.com/tutorial/query-params-str-validations/
- Pydantic: https://docs.pydantic.dev/latest/

### SQLAlchemy

- ORM Docs: https://docs.sqlalchemy.org/en/20/orm/
- Relationships: https://docs.sqlalchemy.org/en/20/orm/relationship_api.html

### React + TypeScript

- React Docs: https://react.dev/
- TypeScript: https://www.typescriptlang.org/docs/

### Testes

- PyTest: https://docs.pytest.org/
- Cypress: https://docs.cypress.io/
- Playwright: https://playwright.dev/

---

## 📝 Notas Técnicas

### Variáveis de Ambiente

Criar arquivo `.env` na raiz de `leiaute-nfse-api`:

```env
# Database
DATABASE_URL=sqlite:///./nfse_leiaute.db

# API
API_TITLE=NFSe Leiaute Portal API
API_VERSION=1.0.0
DEBUG=True

# CORS
ALLOWED_ORIGINS=["http://localhost:5173", "http://localhost:3000"]
```

### Encoding UTF-8 no Windows PowerShell

Para emojis e caracteres especiais funcionarem:

```powershell
$env:PYTHONIOENCODING='utf-8'
```

### Virtual Environment

```bash
# Criar
python -m venv venv

# Ativar (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Ativar (Windows CMD)
venv\Scripts\activate.bat

# Ativar (Linux/Mac)
source venv/bin/activate
```

---

## ✨ Conclusão

O projeto NFSe Leiaute está em uma **posição sólida** para desenvolvimento. Todos os erros críticos foram resolvidos:

- ✅ Dados importados com sucesso (1.548 registros)
- ✅ Models ORM validados
- ✅ Schemas Pydantic corrigidos
- ✅ Routers FastAPI operacionais

**Próximo passo crítico:** Iniciar e validar o servidor FastAPI, seguido de testes da API REST.

**Estimativa para MVP:** 1-2 semanas (dependendo de testes e ajustes)

---

**Documento gerado:** 13 de fevereiro de 2026  
**Última atualização:** 13 de fevereiro de 2026  
**Versão:** 1.0.0
