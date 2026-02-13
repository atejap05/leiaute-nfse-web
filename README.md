# NFSe Leiaute Portal - Sistema Completo

Portal web moderno para consulta do leiaute NFSe (Nota Fiscal de Serviço Eletrônica) com 328 serviços, 677 regras de validação e 112 cenários de exportação.

## 📋 Visão Geral

Este é um projeto **full-stack** com duas aplicações coordenadas:

1. **Backend API** (FastAPI + SQLite)
   - Simples, escalável e bem documentado
   - Processa dados dos JSONs gerados pelas rotinas Python
   - Fornecce **6 rotas de API** principais

2. **Frontend SPA** (React + TypeScript + Vite)
   - Moderno, responsivo e com excelente UX
   - 4 páginas principais para busca e visualização
   - Integrado com API via proxy

---

## 💡 Ideia, Objetivos & Lógica de Funcionamento

### 🎯 O Problema Que Resolvemos

O leiaute NFSe (Nota Fiscal de Serviço Eletrônica) é uma estrutura complexa definida pela RFB/SEFAZ com:

- **328 serviços** diferentes (classificações fiscais)
- **677 regras de validação** em 3 níveis (básico, intermediário, avançado)
- **112 cenários de exportação** (combinações de localidades e contextos)
- **431 campos** na estrutura XML

Essa complexidade torna difícil para desenvolvedores, contadores e auditores:

- 🔍 Encontrar quais regras se aplicam a um serviço específico
- 📋 Validar se um XML de NFSe segue todas as regras obrigatórias
- 🔄 Comparar diferentes cenários e suas diferenças
- 📊 Entender a estrutura completa do leiaute

### 🚀 Solução: Portal Web Interativo

Criamos um **portal de busca e consulta em tempo real** que:

1. **Centraliza os dados** - Todos os 328 serviços, 677 regras e 112 cenários em um único banco de dados SQLite
2. **Facilita a busca** - Procure por código de serviço, número de regra, código de erro
3. **Visualiza relacionamentos** - Veja quais regras se aplicam a cada serviço
4. **Filtra por nível** - Regras básicas (nível 1), intermediárias (nível 2) ou avançadas (nível 3)
5. **Compara cenários** - Entenda diferenças entre contextos de exportação

### 🎓 Objetivos Centrais

| Objetivo                     | Como Alcança                                                  |
| ---------------------------- | ------------------------------------------------------------- |
| **Democratizar acesso**      | Interface amigável sem necessidade de expertise técnica       |
| **Acelerar desenvolvimento** | Busca rápida de regras economiza horas de pesquisa            |
| **Reduzir erros**            | Validação visual de regras garante conformidade NFSe          |
| **Documentar mudanças**      | Quando novos leiautes forem lançados, integração simplificada |
| **Ser agnóstico**            | Backend agnóstico - funciona em qualquer linguagem            |

### 🔄 Lógica de Funcionamento Atual

```
┌─────────────────────────────────────────────────────────────┐
│                      FLUXO COMPLETO                         │
└─────────────────────────────────────────────────────────────┘

1️⃣ CAMADA DE DADOS (Estática)
   ├─ output-source/
   │  └─ Leiaute-nfse-rtc-v1-03-00-2013-nt007/
   │     ├─ 0_MASTER_INDEX.json          (Metadados)
   │     ├─ 1_servicos_incidencia.json   (328 serviços)
   │     ├─ 2_cenarios_exportacao.json   (112 cenários)
   │     ├─ 4_leiaute_dps_nfse.json      (431 campos XML)
   │     └─ 5_regras_validacao_nfse.json (677 regras)
   │
   └─ 🔄 TRANSFORMAÇÃO (Python)
      └─ scripts/import_json_to_db.py
         ├─ Lê todos os JSONs
         ├─ Normaliza estrutura
         ├─ Trata valores NULL
         └─ Insere em 6 tabelas SQLite

2️⃣ CAMADA DE ARMAZENAMENTO (Banco de Dados)
   │
   └─ nfse_leiaute.db (SQLite)
      ├─ servicos (328 registros)
      │  └─ Campos: numero_servico, nome, codigo_tributacao, etc
      │
      ├─ regras (677 registros)
      │  └─ Campos: numero_regra, campo, regra_negocio, codigo_erro, nivel
      │
      ├─ cenarios (112 registros)
      │  └─ Campos: nome, descricao, contexto
      │
      ├─ campos_layout (431 registros)
      │  └─ Campos: caminho_xml, elemento_xml, obrigatorio
      │
      ├─ restricoes (0 registros - dados futuros)
      │  └─ Relaciona campos com regras
      │
      └─ master_index (1 registro)
         └─ Metadados: versão, data, source

3️⃣ CAMADA DE API (Backend FastAPI)
   │
   ├─ GET /api/services
   │  └─ Retorna lista de 328 serviços com paginação
   │
   ├─ GET /api/services/{id}
   │  └─ Detalhes de um serviço + regras aplicáveis
   │
   ├─ GET /api/rules
   │  └─ Lista de 677 regras com filtros (nivel, codigo_erro, campo)
   │
   ├─ GET /api/rules/filtro/por-nivel/{nivel}
   │  └─ Apenas regras do nível especificado (1, 2 ou 3)
   │
   ├─ GET /api/cenarios
   │  └─ Lista de 112 cenários de exportação
   │
   └─ GET /api/search?q=termo
      └─ Busca full-text em serviços, regras e cenários

4️⃣ CAMADA DE APRESENTAÇÃO (Frontend React)
   │
   ├─ 🔍 Página de Busca (Search)
   │  ├─ Campo de entrada com autocomplete
   │  ├─ Resultados combinados (serviços + regras + cenários)
   │  └─ Link direto para detalhes
   │
   ├─ 📊 Página de Serviços (Services)
   │  ├─ Tabela com 328 serviços
   │  ├─ Filtros por código ou nome
   │  ├─ Paginação (10/20/50 itens)
   │  └─ Click para ver todas as regras do serviço
   │
   ├─ ⚖️ Página de Regras (Rules)
   │  ├─ Tabela com 677 regras
   │  ├─ Filtros por nível (1, 2, 3)
   │  ├─ Filtros por código de erro
   │  ├─ Busca em campos específicos
   │  └─ Destaque de severo (nível 1 = crítico)
   │
   └─ 📋 Página de Cenários (Scenarios)
      ├─ Comparação lado-a-lado
      ├─ Diferenças destacadas
      └─ Export para análise

┌─────────────────────────────────────────────────────────────┐
│                    FLUXO DO USUÁRIO                         │
└─────────────────────────────────────────────────────────────┘

User (Dev/Contador) abre: http://localhost:5173
            ↓
Vê página de busca com histórico
            ↓
Digita: "10101" (código de serviço)
            ↓
Frontend faz: GET /api/search?q=10101
            ↓
Backend busca em:
  • servicos (numero_servico LIKE '10101')
  • regras (campo LIKE '10101')
  • cenarios (nome LIKE '10101')
            ↓
Retorna resultados em JSON
            ↓
Frontend renderiza:
  ✅ 1 Serviço encontrado
  ✅ 23 Regras que mencionam este código
  ✅ 5 Cenários relevantes
            ↓
User clica em: "Serviço 10101"
            ↓
Frontend navega para: /services/10101
            ↓
GET /api/services/10101
           ↓
Backend retorna:
{
  "numero_servico": 10101,
  "nome_servico": "Análise de Sistemas",
  "codigo_tributacao": "01.04",
  "regras_aplicaveis": [
    { "numero_regra": 5, "campo": null, ...},
    { "numero_regra": 23, "campo": "descricao_servico", ...},
    ...
  ]
}
            ↓
Frontend renderiza:
  • Informações do serviço em cards
  • Lista de 23 regras com filtros por nível
  • Link para cada regra individual
            ↓
User clica em: "Regra 5"
            ↓
Frontend navega para: /rules/5
            ↓
GET /api/rules/5
           ↓
Backend retorna regra completa com contexto
            ↓
Frontend renderiza:
  • Número da regra
  • Campo afetado (se houver)
  • Mensagem de erro
  • Nível de severidade
  • Serviços que usam esta regra
  • Cenários relevantes
            ↓
User entende: "Regra 5 se aplica a 128 serviços"
            ↓
Pode filtra para ver só as regras de nível 1 (críticas)
```

### 🔌 Integração com Ecosistema Existente

O projeto se integra com:

```
rotinas/
├─ converter_nfse.py      ← Lê Excel do RFB
│  └─ Gera output-source/.../*.json (dados brutos)
│
└─ validar_nfse.py        ← Valida XMLs contra regras
   └─ FUTURO: Usar API deste portal para validação
```

### 📈 Escabilidade & Extensibilidade

O design permite:

- ✅ **Agregar novos leiautes** - Apenas rodar import num novo diretório
- ✅ **Adicionar campos** - Editar JSONs → import automático
- ✅ **Múltiplos usuários** - API stateless, escalável horizontalmente
- ✅ **Cache inteligente** - Dados estáticos, perfeitos para Redis
- ✅ **Mobile-first** - Frontend é SPA responsiva, funciona em qualquer dispositivo

### 🎯 Use Cases Principais

```
1. DESENVOLVEDOR criando integração NFSe
   → Procura "imposto_retido" no portal
   → Vê quais serviços e regras envolvem este campo
   → Cria validações de forma rápida

2. CONTADOR auditando XMLs de NFSe
   → Verifica se um XML segue todas as 677 regras
   → Filtra por nível para priorizar críticos
   → Gera relatório de conformidade

3. GESTOR DE SISTEMA (TI da empresa)
   → Quer entender estrutura completa do leiaute
   → Busca por tipos de erro mais comuns
   → Planeja melhorias no sistema de NF

4. GERENTE DE PROJETO
   → Estimando esforço para nova integração
   → Vê quantas regras cada serviço tem
   → Calcula complexidade de desenvolimento

5. AUDITOR RFB/SEFAZ
   → Validando conformidade de sistemas
   → Consultando especificação técnica
   → Gerando evidências de aderência
```

---

## 🚀 Quick Start (5 minutos)

### Pré-requisitos

- Python 3.8+
- Node.js 18+
- npm ou yarn

### 1. Setup Backend

```bash
cd leiaute-nfse-api

# Criar ambiente virtual
python -m venv venv

# Ativar (Windows)
venv\Scripts\activate
# Ativar (Linux/Mac)
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Importar dados dos JSONs para SQLite
python scripts/import_json_to_db.py

# Rodar servidor
python -m uvicorn app.main:app --reload --port 8000
```

O backend estará em: **http://localhost:8000**

Documentação interativa (Swagger): **http://localhost:8000/docs**

### 2. Setup Frontend

Em **outro terminal**:

```bash
cd leiaute-nfse-ui

# Instalar dependências
npm install

# Rodar servidor dev
npm run dev
```

O frontend estará em: **http://localhost:5173**

### ✅ Pronto!

Abra http://localhost:5173 no navegador e comece a usar.

---

## 📁 Estrutura do Projeto

```
leiaute-nfse-web/
│
├── leiaute-nfse-api/              # Backend FastAPI
│   ├── app/
│   │   ├── main.py                # Aplicação FastAPI
│   │   ├── config.py              # Configurações
│   │   ├── database.py            # SQLAlchemy setup
│   │   ├── models.py              # Modelos ORM e Pydantic
│   │   └── routers/               # Endpoints
│   │       ├── servicos.py        # GET /api/services
│   │       ├── regras.py          # GET /api/rules
│   │       ├── cenarios.py        # GET /api/scenarios
│   │       └── busca.py           # GET /api/search
│   ├── scripts/
│   │   └── import_json_to_db.py   # Importa JSONs → SQLite
│   ├── tests/
│   │   └── test_api.py            # Testes da API
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
│
├── leiaute-nfse-ui/               # Frontend React
│   ├── src/
│   │   ├── components/
│   │   │   └── Layout.tsx         # Container layout
│   │   ├── pages/
│   │   │   ├── SearchPage.tsx     # / (busca)
│   │   │   ├── ServiceDetailPage/ # /services/:codigo
│   │   │   ├── RulesPage.tsx      # /rules
│   │   │   └── ScenariosPage.tsx  # /scenarios
│   │   ├── services/
│   │   │   └── api.ts             # Cliente HTTP
│   │   ├── App.tsx                # Router
│   │   ├── main.tsx               # Entry point
│   │   └── index.css              # Tailwind + estilos
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   ├── package.json
│   └── README.md
│
├── rotinas/                       # (Existente) Scripts de conversão
│   ├── converter_nfse.py          # Excel → JSON
│   └── validar_nfse.py            # Valida JSONs
│
├── output-source/                 # (Existente) JSONs gerados
│   └── Leiaute-nfse-rtc-v1-03-00-2013-nt007/
│       ├── 0_MASTER_INDEX.json
│       ├── 1_servicos_incidencia.json
│       ├── 2_cenarios_exportacao.json
│       ├── 4_leiaute_dps_nfse.json
│       ├── 5_regras_validacao_nfse.json
│       └── ...
│
├── .gitignore
├── README.md                      # Este arquivo
└── ARCHITECTURE.md                # (Próximo passo) Detalhes técnicos
```

---

## 📚 Documentação Detalhada

Cada aplicação tem seu own `README.md` com mais detalhes:

- [Backend API README](leiaute-nfse-api/README.md) - Endpoints, configuração, testes
- [Frontend SPA README](leiaute-nfse-ui/README.md) - Componentes, routing, deployment

---

## 🔄 Fluxo de Dados

```
User abre http://localhost:5173
        ↓
React Router carrega SearchPage
        ↓
User digita "análise"
        ↓
API Client faz: GET /api/search?q=análise
        ↓
Proxy Vite redireciona para http://localhost:8000/api/search?q=análise
        ↓
FastAPI busca em SQLite
        ↓
Retorna JSON com resultados
        ↓
React renderiza ResultadosList
```

---

## 🧪 Testes

### Backend

```bash
cd leiaute-nfse-api
pytest tests/ -v
```

### Frontend

```bash
cd leiaute-nfse-ui
npm test
```

---

## 🚀 Produção

### Deploy do Backend

**Docker:**

```bash
cd leiaute-nfse-api
docker build -t nfse-api .
docker run -p 8000:8000 nfse-api
```

**Heroku:**

```bash
heroku create nfse-api
git push heroku main
```

### Deploy do Frontend

**Vercel (Recomendado):**

```bash
cd leiaute-nfse-ui
npm i -g vercel
vercel
```

**Netlify:**

```bash
cd leiaute-nfse-ui
npm run build
# Fazer deploy da pasta 'dist'
```

---

## 📊 Dados & Performance

### Quantidade de Dados

- **328 Serviços** (códigos 10101-20405)
- **677 Regras de Validação** (níveis 1/2/3)
- **112 Cenários de Exportação** (combinações localidades)
- **431 Campos Leiaute** (estrutura XML)

### Performance Esperada

- Busca em 328 serviços: **< 100ms**
- Busca em 677 regras: **< 200ms**
- Listar 20 itens: **< 50ms**
- Todas as requisições com índices otimizados

---

## 🔧 Configuração

### Backend Variáveis de Ambiente

Crie `leiaute-nfse-api/.env`:

```env
DEBUG=True
API_TITLE=NFSe Leiaute Portal API
API_VERSION=1.0.0
DATABASE_URL=sqlite:///./nfse_leiaute.db
SOURCE_DIR=../output-source/Leiaute-nfse-rtc-v1-03-00-2013-nt007
```

### Frontend Configuração

O arquivo `vite.config.ts` configura automaticamente:

- Proxy `/api` → `http://localhost:8000/api`
- Alias `@/` → `src/`
- Tailwind CSS
- TypeScript paths

---

## 🎯 Próximos Passos (Roadmap)

### Fase 1 ✅ (Atual)

- [x] Backend FastAPI com SQLite
- [x] Frontend React + Vite
- [x] Importação de dados JSON
- [x] Rotas API básicas
- [x] Testes unitários

### Fase 2 (Próximo)

- [ ] CI/CD com GitHub Actions
- [ ] Deploy automático (Vercel + Heroku)
- [ ] Testes E2E (Cypress)
- [ ] Performance optimization
- [ ] Analytics (Plausible)

### Fase 3 (Futuro)

- [ ] Authentication (JWT)
- [ ] Database migrations (Alembic)
- [ ] Webhook para novos leiautes
- [ ] Export de dados (CSV/PDF)
- [ ] Notificações de mudanças

---

## 🆘 Troubleshooting

### Backend não conecta

```bash
# Verifique se FastAPI está rodando
curl http://localhost:8000/health

# Se falhar, rode novamente:
python -m uvicorn app.main:app --reload --port 8000
```

### Frontend não vee API

```bash
# Verifique proxy em vite.config.ts
# Deve redirecionar /api para http://localhost:8000/api
```

### Import de dados falha

```bash
# Verifique se JSONs existem
ls output-source/Leiaute-nfse-rtc-v1-03-00-2013-nt007/

# Tente reimportar:
python scripts/import_json_to_db.py --source-dir ../output-source/Leiaute-nfse-rtc-v1-03-00-2013-nt007
```

---

## 📞 Contato & Support

- 📧 Issues: GitHub Issues (se houver repo público)
- 📚 Documentação: Veja READMEs de cada aplicação
- 🐛 Bugs: Reporte com stack trace completo

---

## 📄 Licença

Dados do leiaute vêm de especificações técnicas **RFB/SEFAZ** (Governo Brasileiro).

Código da aplicação: MIT License

---

**Status**: 🟢 **Em Desenvolvimento - Fase 1 Completa**

Última atualização: **Fevereiro 13, 2026**
