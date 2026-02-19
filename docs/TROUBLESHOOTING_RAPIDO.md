# Troubleshooting Rapido

Guia objetivo para diagnostico dos problemas mais frequentes.

## 1. Startup rapido

Backend:
```bash
cd leiaute-nfse-api
python -m uvicorn app.main:app --reload --port 8000
```

Frontend:
```bash
cd leiaute-nfse-ui
npm run dev
```

Verificacoes:
- API: `http://localhost:8000/health`
- Swagger: `http://localhost:8000/docs`
- Frontend: `http://localhost:5173`

## 2. Erros comuns

### Erro: `Cannot read properties of undefined (reading 'length')`
Contexto:
- fluxo de busca no frontend

Causa provavel:
- payload sem `items`

Acao:
- confirmar se `api.search()` esta normalizando `resultados` -> `items`

### Erro: `No module named pytest`
Causa:
- ambiente Python ativo sem dependencias instaladas

Acao:
```bash
cd leiaute-nfse-api
pip install -r requirements.txt
```

### Erro de build em `vite.config.ts` (`path`/`__dirname`)
Causa:
- configuracao TS/Node incompleta

Acao:
- validar `tsconfig.node.json`
- garantir tipos Node disponiveis

### API retorna 422 em busca curta
Causa:
- parametro `q` exige minimo de 2 caracteres

Acao:
- enviar query com 2+ caracteres

## 3. Comandos de diagnostico

### Conferir endpoints da API
```bash
curl http://localhost:8000/health
curl "http://localhost:8000/api/search?q=importacao&limit=30"
curl "http://localhost:8000/api/services?limit=5"
```

### Conferir banco SQLite
```bash
python - << 'PY'
import sqlite3
conn = sqlite3.connect('leiaute-nfse-api/nfse_leiaute.db')
cur = conn.cursor()
for t in ['servicos','regras','cenarios','campos_layout']:
    cur.execute(f'SELECT COUNT(*) FROM {t}')
    print(t, cur.fetchone()[0])
conn.close()
PY
```

### Rodar testes backend
```bash
cd leiaute-nfse-api
pytest -v
```

## 4. Checklist antes de abrir bug

- reproduziu o erro com passos claros
- coletou endpoint/rota afetada
- capturou request/response relevante
- incluiu log com `request_id` quando disponivel

## 5. Escalonamento

Se o problema persistir:
1. anexar stack trace e logs estruturados
2. informar commit/branch
3. informar se ocorre em backend, frontend ou integracao
