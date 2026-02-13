# NFSe Leiaute Portal UI - Frontend React

Portal web moderno para consulta do leiaute NFSe com busca rápida, visualização de regras e comparação de cenários.

## 🚀 Quick Start

### 1. Setup Inicial

```bash
# Instalar dependências
npm install

# Ou com yarn
yarn install
```

### 2. Configurar Proxy da API

O arquivo `vite.config.ts` já configura proxy para `/api` → `http://localhost:8000`.

Certifique-se de que o backend FastAPI está rodando em `http://localhost:8000`.

### 3. Rodar em Desenvolvimento

```bash
npm run dev

# Acesse: http://localhost:5173
```

### 4. Build para Produção

```bash
npm run build

# Preview do build
npm run preview
```

## 📁 Estrutura do Projeto

```
leiaute-nfse-ui/
├── src/
│   ├── components/
│   │   └── Layout.tsx              # Layout container com header/footer
│   ├── pages/
│   │   ├── SearchPage.tsx          # Busca unificada (serviços, regras, campos)
│   │   ├── ServiceDetailPage.tsx   # Detalhe de serviço + regras
│   │   ├── RulesPage.tsx           # Lista de regras com filtros
│   │   └── ScenariosPage.tsx       # Cenários de exportação
│   ├── services/
│   │   └── api.ts                  # Cliente HTTP (Axios) para API
│   ├── App.tsx                     # Componente raiz com Router
│   ├── main.tsx                    # Entry point
│   └── index.css                   # Tailwind + componentes globais
├── vite.config.ts                  # Configuração Vite
├── package.json
├── tsconfig.json
├── tailwind.config.js
├── postcss.config.js
└── index.html
```

## 🎨 UI/UX Features

- ✅ **Responsivo**: Mobile-first, funciona em tablets e desktops
- ✅ **Dark Mode Ready**: Componentes com suporte a dark mode
- ✅ **Acessibilidade**: Semântica HTML correta, ARIA labels
- ✅ **Performance**: Code splitting, lazy loading, otimizações Vite
- ✅ **Modern Design**: Tailwind CSS, componentes minimalistas
- ✅ **Rápido**: Busca em tempo real com debounce

## 📖 Páginas

### 1. SearchPage (`/`)

- Campo única de busca com autocompletar
- Busca em: serviços (descrição), regras (regra, código erro, número), campos
- Resultados agrupados por tipo
- Score de relevância visual

### 2. ServiceDetailPage (`/services/:codigo`)

- Detalhes completos do serviço
- Localidade de incidência (LC 116/03)
- Regras aplicáveis ao serviço
- Grupos de informação

### 3. RulesPage (`/rules`)

- Lista paginada de 677 regras
- Filtros: nível (1/2/3), campo
- Visualização clara de regra + mensagem de erro
- Contexto e níveis destacados por cor

### 4. ScenariosPage (`/scenarios`)

- 112 cenários de exportação
- Filtros: Brasil-Brasil, Exportação
- Visualização clara de localidades
- Informações de ISSQN e Comex

## 🔄 Fluxo de Dados

```
User Input
    ↓
SearchPage (componente)
    ↓
api.search() (services/api.ts)
    ↓
HTTP GET /api/search?q=termo
    ↓
FastAPI Backend
    ↓
SQLite Database
    ↓
JSON Response
    ↓
React setState()
    ↓
Render resultados
```

## 🎯 Componentes Reutilizáveis

Todos os componentes usam **Tailwind CSS** com classes globais definidas em `index.css`:

```html
<!-- Botão -->
<button className="btn-primary">Clique aqui</button>

<!-- Input -->
<input className="input-base" />

<!-- Card -->
<div className="card">Conteúdo</div>

<!-- Badge -->
<span className="badge badge-primary">Label</span>
```

## 🧪 Testes

```bash
# Rodar testes
npm run test

# Com UI
npm run test:ui
```

## 🔧 Configurações

### Environment Variables

Crie um arquivo `.env` (não necessário para dev):

```bash
VITE_API_BASE_URL=http://localhost:8000/api
```

### Tailwind Customization

Edite `tailwind.config.js` para customizar cores, fontes, etc.

## 📦 Dependências

| Pacote             | Uso         |
| ------------------ | ----------- |
| `react`            | Framework   |
| `react-router-dom` | Roteamento  |
| `axios`            | HTTP client |
| `lucide-react`     | Icons       |
| `tailwindcss`      | Styling     |
| `vite`             | Build tool  |
| `typescript`       | Type safety |

## 🚀 Deploy

### Vercel (Recomendado)

```bash
# Instalar CLI
npm i -g vercel

# Deploy
vercel
```

### Netlify

```bash
# Build
npm run build

# Fazer deploy da pasta 'dist'
```

### Docker

```dockerfile
# Build stage
FROM node:18 as builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

## 🐛 Troubleshooting

### CORS Error

Verifique se FastAPI está com CORS habilitado e rodando em `http://localhost:8000`.

### 404 ao acessar /api

Verifique proxy em `vite.config.ts`. Certifique-se que backend está rodando.

### Componentes não carregam

Verifique imports. Use `@/` para absolute imports (path alias configurado em `tsconfig.json`).

## 📝 Licença

Dados do leiaute vêm de especificações técnicas RFB/SEFAZ.

---

**Última atualização**: Fevereiro 2026
