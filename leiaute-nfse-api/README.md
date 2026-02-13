# NFSe Leiaute API - Backend FastAPI

API REST construída com FastAPI para servir dados do leiaute NFSe com 328 serviços, 677 regras de validação e 112 cenários de exportação.

## 🚀 Quick Start

### 1. Setup Inicial

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente (Windows)
venv\Scripts\activate

# Ativar ambiente (Linux/Mac)
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### 2. Configurar Variáveis de Ambiente

```bash
# Copiar arquivo de exemplo
cp .env.example .env

# Editar .env conforme necessário
```

### 3. Importar Dados

```bash
# Importa JSONs do output-source para SQLite
python scripts/import_json_to_db.py

# Com diretório customizado:
python scripts/import_json_to_db.py --source-dir /caminho/para/json
```

### 4. Rodar o Servidor

```bash
# Desenvolvimento com reload automático
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Verificar em: http://localhost:8000
# Documentação (Swagger): http://localhost:8000/docs
```

## 📋 Endpoints Principais

### Serviços

- `GET /api/services` - Lista serviços com paginação
- `GET /api/services/{codigo}` - Detalhe de um serviço
- `GET /api/services/{codigo}/rules` - Regras aplicáveis a um serviço

### Regras

- `GET /api/rules` - Lista regras com filtros
- `GET /api/rules/{numero}` - Detalhe de uma regra
- `GET /api/rules/filtro/por-nivel/{nivel}` - Regras por nível (1, 2, 3)
- `GET /api/rules/filtro/por-erro/{codigo_erro}` - Regras por código de erro

### Cenários

- `GET /api/scenarios` - Lista cenários
- `GET /api/scenarios/{numero}` - Detalhe de um cenário
- `POST /api/scenarios/compare` - Compara múltiplos cenários
- `GET /api/scenarios/filtro/brasil-brasil` - Cenários domésticos
- `GET /api/scenarios/filtro/exportacao` - Cenários de exportação

### Busca

- `GET /api/search?q=termo` - Busca unificada (serviços, regras, campos)
- `GET /api/search/codigo/{codigo}` - Busca por código de serviço
- `GET /api/search/erro/{codigo_erro}` - Busca por código de erro

### Health

- `GET /health` - Health check
- `GET /` - Info sobre a API

## 🧪 Testes

```bash
# Rodar todos os testes
pytest

# Rodar com verbosidade
pytest -v

# Rodar um arquivo específico
pytest tests/test_api.py -v

# Com cobertura
pytest --cov=app tests/
```

## 📁 Estrutura do Projeto

```
leiaute-nfse-api/
├── app/
│   ├── __init__.py
│   ├── config.py           # Configurações
│   ├── database.py         # Setup SQLAlchemy
│   ├── models.py           # Modelos ORM e Pydantic
│   ├── main.py             # Aplicação FastAPI
│   └── routers/
│       ├── servicos.py     # Endpoints de serviços
│       ├── regras.py       # Endpoints de regras
│       ├── cenarios.py     # Endpoints de cenários
│       └── busca.py        # Endpoints de busca
├── scripts/
│   └── import_json_to_db.py # Script de importação
├── tests/
│   └── test_api.py         # Testes da API
├── requirements.txt        # Dependências Python
└── README.md              # Este arquivo
```

## 💾 Base de Dados

### Tabelas Criadas

1. **servicos** (328 registros)
   - código_tributacao (PK, índex)
   - descricao
   - campos de localidade de incidência
   - índices para busca rápida

2. **regras** (677 registros)
   - numero_regra (índex)
   - campo
   - codigo_erro (índex)
   - nivel_regra (índex 1-3)
   - mensagem_erro
   - FK para serviço

3. **cenarios** (112 registros)
   - numero_cenario (PK, índex)
   - localidades (tomador, intermediário, prestação)
   - info de exportação/comex

4. **campos_layout** (431 registros)
   - numero_campo (índex)
   - caminho_xml (índex)
   - tipo_dado, ocorrencia, tamanho

5. **restricoes**
   - Valores permitidos para campos
   - Limites e validações

6. **master_index**
   - Metadados da versão do leiaute

## 🔧 Configuração

### Variáveis de Ambiente (.env)

```env
# API
DEBUG=True
API_TITLE=NFSe Leiaute Portal API
API_VERSION=1.0.0

# Database
DATABASE_URL=sqlite:///./nfse_leiaute.db

# Source (JSONs)
SOURCE_DIR=../output-source/Leiaute-nfse-rtc-v1-03-00-2013-nt007
```

## 🔍 Exemplos de Uso

### Buscar um serviço

```bash
curl "http://localhost:8000/api/services/10101"
```

### Listar regras com filtro

```bash
curl "http://localhost:8000/api/rules?nivel=1&limit=10"
```

### Buscar por texto

```bash
curl "http://localhost:8000/api/search?q=análise"
```

### Comparar cenários

```bash
curl -X POST "http://localhost:8000/api/scenarios/compare?cenarios_ids=1&cenarios_ids=2&cenarios_ids=3"
```

## 📝 Notas

- Banco SQLite é criado automaticamente na primeira execução
- Índices otimizados para buscas de serviços e regras
- Paginação limitada a 100 itens por página (protege recursos)
- CORS habilitado para localhost durante desenvolvimento

## 🚀 Deploy

### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY scripts ./scripts

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Executar com Docker

```bash
docker build -t nfse-api .
docker run -p 8000:8000 -e DEBUG=False nfse-api
```

## 📚 Documentação da API

Acesse `http://localhost:8000/docs` para ver a documentação interativa (Swagger UI).

## 🤝 Contribuindo

1. Fazer alterações
2. Rodar testes: `pytest`
3. Verificar cobertura: `pytest --cov=app`
4. Commit com mensagem clara

## 📄 Licença

Todos os dados (JSONs) vêm de especificações técnicas governamentais (RFB/SEFAZ).

---

**Última atualização**: Fevereiro 2026
