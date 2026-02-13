# 🔧 Guia Prático de Troubleshooting - API NFSe

**Referência Rápida para Diagnóstico e Resolução de Problemas Comuns**

---

## 🚀 Quick Start Checklist

Ao iniciar o desenvolvimento, execute esta sequência:

```bash
# 1. Verificar Python
python --version  # Esperado: 3.11+

# 2. Ativar Virtual Environment
cd leiaute-nfse-api
.\venv\Scripts\Activate.ps1

# 3. Verificar Dependências
pip list | findstr FastAPI
pip list | findstr SQLAlchemy
pip list | findstr Pydantic

# 4. Verificar Banco de Dados
ls nfse_leiaute.db  # Deve existir

# 5. Testar Importação de App
python -c "from app.main import app; print('✅ App OK')"

# 6. Iniciar Servidor
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 7. Em outro terminal, testar
curl http://localhost:8000/health
```

---

## 🔴 Problemas Comuns e Soluções

### Problema 1: ModuleNotFoundError: No module named 'app'

#### Sintoma

```
ModuleNotFoundError: No module named 'app'
```

#### Diagnóstico

```bash
# Verificar se está no diretório certo
pwd  # Deve ser: .../leiaute-nfse-web/leiaute-nfse-api

# Verificar se pasta 'app' existe
ls app/

# Verificar se __init__.py existe
ls app/__init__.py
```

#### Soluções (em ordem de probabilidade)

**Solução 1: Diretório Incorreto**

```bash
# ❌ ERRADO - raiz do projeto
cd leiaute-nfse-web
python -m uvicorn app.main:app  # FALHA

# ✅ CORRETO - dentro do backend
cd leiaute-nfse-web/leiaute-nfse-api
python -m uvicorn app.main:app  # OK
```

**Solução 2: Virtual Environment Não Ativado**

```bash
# Verificar se venv está ativado
# Look for (venv) no prompt do PowerShell

# Se não estiver, ativar:
.\venv\Scripts\Activate.ps1
```

**Solução 3: PYTHONPATH Não Configurado**

```bash
# Opção A: Conforme startup
$env:PYTHONPATH='C:\Users\[USERNAME]\Documents\My-Dev-Workspace\Projetos\Git_Projects\leiaute-nfse-web\leiaute-nfse-api'
python -m uvicorn app.main:app --reload

# Opção B: Mudar para diretório do projeto
cd leiaute-nfse-api
python -m uvicorn app.main:app --reload

# Opção C: Usar caminho relativo
cd leiaute-nfse-web
cd leiaute-nfse-api
python -m uvicorn app.main:app --reload
```

---

### Problema 2: NOT NULL constraint failed: regras.CAMPO

#### Sintoma

```
sqlite3.IntegrityError: NOT NULL constraint failed: regras.campo
```

Ocorre ao executar `python scripts/import_json_to_db.py`

#### Causa Raiz

A origem JSON tem campos com valor `NULL`, mas o ORM não permite NULLs.

#### Exemplo

```json
{
  "numero_regra": 5,
  "campo": null,  // ← Este NULL causa o erro
  "regra_negocio": "Validação XYZ",
  ...
}
```

#### Solução Permanente

Editar `leiaute-nfse-api/app/models.py`:

```python
# Encontrar a classe RegraORM (linha ~40)
class RegraORM(Base):
    __tablename__ = "regras"

    # ✅ TODOS os campos opcionais devem ter nullable=True
    campo = Column(String(255), nullable=True)  # ← Chave
    regra_negocio = Column(Text, nullable=True)
    codigo_erro = Column(String(10), nullable=True)
    mensagem_erro = Column(Text, nullable=True)
    nivel_regra = Column(Integer, nullable=True)
```

#### Validação

```bash
# Deletar DB antigo e reimportar
rm nfse_leiaute.db
python scripts/import_json_to_db.py

# Esperado:
# ✅ Importación concluida com sucesso!
# ✅ Serviços: 328
# ✅ Regras: 677
```

#### Diagnóstico Avançado

Se continuar falhando, identificar qual campo exatamente:

```python
# Adicionar ao import_json_to_db.py
null_fields = {k: v for k, v in regra_dict.items() if v is None}
if null_fields:
    print(f"⚠️ Regra #{regra_dict['numero_regra']} NULLs: {list(null_fields.keys())}")

# Executar:
python scripts/import_json_to_db.py 2>&1 | grep "NULLS:"
```

---

### Problema 3: PydanticUndefinedAnnotation: name 'X' is not defined

#### Sintoma

```
PydanticUndefinedAnnotation: name 'RegraResponse' is not defined
```

Ocorre ao iniciar o servidor FastAPI

#### Causa Raiz

Forward references em modelos Pydantic sem proper setup

#### Solução Rápida

**Passo 1:** Primeiro arquivo do models.py deve ter:

```python
# ✅ LINHA 1 - OBRIGATÓRIO
from __future__ import annotations
```

**Passo 2:** Final do arquivo models.py deve ter:

```python
# ✅ LINHA ~361 - OBRIGATÓRIO
ServicoDetail.model_rebuild()
```

**Passo 3:** Campos com valores opcionais:

```python
# ✅ CORRETO
class RegraBase(BaseModel):
    campo: Optional[str] = None  # Pode ser indefinido
    numero_regra: int  # Obrigatório
```

#### Validação

```bash
python -c "from app.models import ServicoDetail; print('✅ Models OK')"
```

---

### Problema 4: AssertionError: Cannot use `Query` for path param 'X'

#### Sintoma

```
AssertionError: Cannot use `Query` for path param 'nivel'.
```

Ocorre ao carregar routers no FastAPI

#### Causa Raiz

Parâmetro de caminho (`{nivel}`) usando decorator `Query()` em vez de `Path()`

#### Comparação

```python
# ❌ ERRADO - Query é para ?param=value
@router.get("/filtro/por-nivel/{nivel}")
def get_rules(nivel: int = Query(...)):
    # URL seria: /filtro/por-nivel/{nivel}?nivel=3  ← absurdo!
    pass

# ✅ CORRETO - Path é para /param/value
@router.get("/filtro/por-nivel/{nivel}")
def get_rules(nivel: int = Path(...)):
    # URL é: /filtro/por-nivel/3  ← correto!
    pass
```

#### Buscar Erros no Projeto

```bash
# Procurar todas as definições de rotas
grep -r "def get_rules" leiaute-nfse-api/app/routers/

# Procurar por Query em path params
grep -B2 "Query(...)" leiaute-nfse-api/app/routers/*.py | grep "@router"
```

#### Solução

Em cada arquivo router, validar:

```python
# ✅ Importação correta
from fastapi import APIRouter, Path, Query

# ✅ Path parameter
@router.get("/{id}")
def get_item(id: int = Path(..., gt=0)):
    pass

# ✅ Query parameter
@router.get("/search")
def search(q: str = Query(..., min_length=1)):
    pass

# ✅ Body parameter
@router.post("/create")
def create(item: ItemModel):  # Sem decorator
    pass
```

---

### Problema 5: Encoding Issues - Emojis Não Aparecem

#### Sintoma

```
UnicodeEncodeError: 'cp1252' codec can't encode character
# ou emojis aparecem como ??????
```

#### Causa

Terminal Windows usando encoding Latin-1 em vez de UTF-8

#### Solução Rápida

```powershell
# Adicionar ao comando
$env:PYTHONIOENCODING='utf-8'

# Exemplo:
$env:PYTHONIOENCODING='utf-8'; python scripts/import_json_to_db.py
```

#### Solução Permanente

Adicionar ao perfil PowerShell:

```powershell
# Abrir
$PROFILE

# Adicionar
$env:PYTHONIOENCODING='utf-8'

# Salvar (Ctrl+S)
```

#### Verificação

```bash
python -c "[System.Console]::OutputEncoding = [System.Text.Encoding]::UTF8; print('✅ UTF-8 OK')"
```

---

### Problema 6: Database Lock - sqlite3.OperationalError: database is locked

#### Sintoma

```
sqlite3.OperationalError: database is locked
```

#### Causa

Múltiplos processos acessando SQLite simultaneamente

#### Solução Imediata

```bash
# 1. Killall processos Python
Get-Process python | Stop-Process

# 2. Verificar se DB está intacto
cd leiaute-nfse-api
python -c "import sqlite3; conn = sqlite3.connect('nfse_leiaute.db'); print('✅ DB OK')"

# 3. Recriar se necessário
rm nfse_leiaute.db
python scripts/import_json_to_db.py
```

#### Prevenção

```python
# Em database.py, adicionar timeout
import sqlite3

# Aumentar timeout para SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./nfse_leiaute.db?timeout=30"
```

---

## 📊 Testes de Validação

### Teste 1: Health Check

```bash
# Esperado: Status 200
curl -v http://localhost:8000/health

# Saída esperada:
# < HTTP/1.1 200 OK
# {"status": "healthy"}
```

### Teste 2: Listar Serviços

```bash
curl "http://localhost:8000/api/services?limit=2&offset=0"

# Saída esperada:
# {
#   "total": 328,
#   "limit": 2,
#   "offset": 0,
#   "items": [...]
# }
```

### Teste 3: Detalhe de Serviço

```bash
# Listar primeiro para pegar um ID válido
curl "http://localhost:8000/api/services/1"

# Esperado: Status 200 com dados do serviço
```

### Teste 4: Regras por Nível

```bash
curl "http://localhost:8000/api/rules/filtro/por-nivel/1?limit=5"

# Esperado: Lista de regras nível 1
```

### Teste 5: Busca

```bash
curl "http://localhost:8000/api/search?q=nfse"

# Esperado: Resultados de busca
```

### Teste 6: Erro 404

```bash
curl "http://localhost:8000/api/services/99999"

# Esperado: Status 404, mensagem: "Serviço não encontrado"
```

---

## 🐛 Debug Mode

### Habilitar logging detalhado

```python
# Em leiaute-nfse-api/app/main.py, adicionar:
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
```

### Verificar SQL gerado

```python
# Em database.py
from sqlalchemy import event
from sqlalchemy.engine import Engine

@event.listens_for(Engine, "before_cursor_execute")
def receive_before_cursor_execute(conn, cursor, statement, params, context, executemany):
    print(f"🔍 SQL: {statement}")
    print(f"   Params: {params}")
```

### Inspecionar dados do banco

```bash
# Ver estrutura das tabelas
cd leiaute-nfse-api
python

# No Python:
import sqlite3
conn = sqlite3.connect('nfse_leiaute.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
print(cursor.fetchall())

# Ver dados de uma tabela
cursor.execute("SELECT COUNT(*) FROM regras")
print(cursor.fetchone())

# Ver um exemplo
cursor.execute("SELECT * FROM regras LIMIT 1")
print(cursor.fetchone())
```

---

## 📋 Checklist de Deployment

Antes de subir para produção:

- [ ] Todos os testes passando (`pytest tests/`)
- [ ] Cobertura de código > 80%
- [ ] Sem warnings no linting (`flake8`)
- [ ] Type checking passando (`mypy`)
- [ ] .env configurado com secrets
- [ ] CORS configurado apenas para domínios permitidos
- [ ] Database migrado para PostgreSQL
- [ ] Backup automático configurado
- [ ] Logging e alertas configurados
- [ ] Rate limiting habilitado
- [ ] HTTPS/SSL configurado
- [ ] Health check endpoint funcionando

---

## 🌐 URLs Úteis para Desenvolvimento

| Recurso      | URL                                  |
| ------------ | ------------------------------------ |
| API Health   | `http://localhost:8000/health`       |
| Swagger Docs | `http://localhost:8000/docs`         |
| ReDoc        | `http://localhost:8000/redoc`        |
| OpenAPI JSON | `http://localhost:8000/openapi.json` |
| Services API | `http://localhost:8000/api/services` |
| Rules API    | `http://localhost:8000/api/rules`    |
| Frontend Dev | `http://localhost:5173`              |

---

## 💾 Respostas Esperadas Padrão

### Sucesso (200)

```json
{
  "total": 328,
  "limit": 10,
  "offset": 0,
  "items": [...]
}
```

### Error (4xx)

```json
{
  "detail": "Mensagem de erro clara"
}
```

### Error (5xx)

```json
{
  "detail": "Internal server error",
  "trace_id": "uuid-para-logging"
}
```

---

## 📞 Contatos Úteis

Para mais informações:

- FastAPI: https://fastapi.tiangolo.com/
- SQLAlchemy: https://docs.sqlalchemy.org/
- Pydantic: https://docs.pydantic.dev/
- Project Docs: `./docs/`

---

**Última atualização:** 13 de fevereiro de 2026
