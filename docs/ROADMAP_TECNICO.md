# 🗺️ Roadmap Técnico Detalhado - NFSe Leiaute Portal

**Planejamento de Milestones, Tasks Técnicas e Métricas de Sucesso**

---

## 📅 Visão Geral da Timeline

```
FEV 2026
├─ Semana 1: ✅ Data Import (CONCLUÍDO)
│  └─ 328 services + 677 rules + 112 scenarios importados
│
├─ Semana 2: 🔄 Backend Stabilization (ATUAL)
│  ├─ Validar API endpoints
│  ├─ Implementar testes
│  └─ Fix issues de inicialização
│
├─ Semana 3: ▶️ Frontend Integration (PRÓXIMO)
│  ├─ React + TypeScript setup
│  ├─ Service layer (API client)
│  └─ UI components básicos
│
└─ Semana 4: ▶️ Polish & Testing (FUTURO)
   ├─ E2E tests
   ├─ Performance optimization
   └─ MVP Release
```

---

## 🎯 Milestone 1: Backend Stability (Next 3-5 dias)

### Objetivo

Ter servidor FastAPI 100% funcional e testado

### Tasks

#### Task 1.1: Start & Validate Server ⏱️ 1-2 horas

**Subtasks:**

- [ ] Iniciar servidor sem erros

  ```bash
  cd leiaute-nfse-api
  python -m uvicorn app.main:app --reload
  ```

  **Sucesso:** Logs mostram `Application startup complete`

- [ ] Acessar Swagger UI
  - URL: `http://localhost:8000/docs`
  - **Sucesso:** Página Swagger abre e lista 17 endpoints HTTP (15 em `/api` + `/health` + `/`)

- [ ] Testar health endpoint
  ```bash
  curl http://localhost:8000/health
  ```
  **Sucesso:** Resposta `{"status": "healthy"}`

**Bloqueadores Conhecidos:**

- ModuleNotFoundError → Usar `cd leiaute-nfse-api` antes de rodar
- Encoding issues → Set `$env:PYTHONIOENCODING='utf-8'`

---

#### Task 1.2: Unit Tests para Models ⏱️ 2-3 horas

**Arquivo:** `leiaute-nfse-api/tests/test_models.py`

**Testes a Implementar:**

```python
def test_servico_model():
    """RegraORM com campos opcionais"""
    assert RegraORM.campo.default is None
    assert RegraORM.regra_negocio.nullable == True

def test_pydantic_forward_refs():
    """ServicoDetail resolve forward references"""
    detail = ServicoDetail(...)
    assert isinstance(detail.regras, list)

def test_nullable_fields():
    """Todos os campos opcionais aceitam None"""
    regra = RegraORM(numero_regra=1, campo=None)
    assert regra.campo is None
```

**Validação:**

```bash
pytest tests/test_models.py -v
```

**Sucesso esperado:**

```
test_models.py::test_servico_model PASSED
test_models.py::test_pydantic_forward_refs PASSED
test_models.py::test_nullable_fields PASSED
======================== 3 passed in 0.15s ========================
```

---

#### Task 1.3: Integration Tests para Routers ⏱️ 3-4 horas

**Arquivo:** `leiaute-nfse-api/tests/test_routers.py`

**Testes a Implementar:**

```python
# test_servicos.py
def test_list_services_returns_paginated_data():
    response = client.get("/api/services?limit=10&offset=0")
    assert response.status_code == 200
    assert "total" in response.json()
    assert response.json()["total"] == 328

def test_get_service_detail():
    response = client.get("/api/services/1")
    assert response.status_code == 200
    assert response.json()["numero_servico"]

def test_service_not_found():
    response = client.get("/api/services/99999")
    assert response.status_code == 404

# test_regras.py
def test_list_rules():
    response = client.get("/api/rules?limit=5")
    assert response.status_code == 200
    assert len(response.json()["items"]) <= 5

def test_rules_by_nivel():
    response = client.get("/api/rules/filtro/por-nivel/1?limit=5")
    assert response.status_code == 200
    assert all(r["nivel_regra"] == 1 for r in response.json()["items"])

def test_rules_filter_codigo_erro():
    response = client.get("/api/rules?codigo_erro=E1260")
    assert response.status_code == 200
    items = response.json()["items"]
    assert all("E1260" in r.get("codigo_erro", "") for r in items if r.get("codigo_erro"))

# test_cenarios.py
def test_list_cenarios():
    response = client.get("/api/cenarios?limit=10")
    assert response.status_code == 200
    assert response.json()["total"] == 112

# test_busca.py
def test_search_returns_results():
    response = client.get("/api/search?q=nfse")
    assert response.status_code == 200
    assert "results" in response.json()

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
```

**Validação:**

```bash
pytest tests/test_routers.py -v --cov=app --cov-report=html
```

**Sucesso esperado:**

```
========================== 10 passed in 2.34s ==========================
Coverage: 85%
```

---

#### Task 1.4: Database Integrity Check ⏱️ 30 minutos

**Script:** `leiaute-nfse-api/scripts/check_db_integrity.py`

```python
import sqlite3
from pathlib import Path

def check_database():
    db_path = Path("nfse_leiaute.db")
    assert db_path.exists(), "Database file not found"

    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    # Check tables exist
    tables = ["servicos", "regras", "cenarios", "campos_layout", "restricoes", "master_index"]
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"✅ {table}: {count} records")

    # Check foreign keys
    cursor.execute("PRAGMA foreign_key_list(regras)")
    fks = cursor.fetchall()
    print(f"✅ Foreign keys: {len(fks)}")

    # Check indexes
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index'")
    indexes = cursor.fetchall()
    print(f"✅ Indexes: {len(indexes)}")

    conn.close()

if __name__ == "__main__":
    check_database()
```

**Sucesso esperado:**

```
✅ servicos: 328 records
✅ regras: 677 records
✅ cenarios: 112 records
✅ campos_layout: 431 records
✅ restricoes: 0 records
✅ master_index: 1 record
✅ Foreign keys: 1
✅ Indexes: 7
```

---

#### Task 1.5: Documentation Validation ⏱️ 1 hora

**Checklist:**

- [ ] Swagger `/docs` carrega corretamente
- [ ] ReDoc `/redoc` carrega
- [ ] OpenAPI JSON `/openapi.json` válido
- [ ] Cada endpoint tem description
- [ ] Parâmetros documentados
- [ ] Response models documentados

**Validação:**

```bash
# Em http://localhost:8000/docs:
# - Verificar todos os 17 endpoints HTTP listados
# - Clicar em "Try it out" em 3 endpoints
# - Validar responses
```

---

### Métricas de Sucesso - Milestone 1

| Métrica                   | Esperado | Atual |
| ------------------------- | -------- | ----- |
| **Server startup time**   | < 2s     | ?     |
| **Test coverage**         | > 80%    | ?     |
| **API endpoints working** | 15/15    | ?     |
| **Database integrity**    | 100%     | ✅    |
| **Documentation**         | Complete | ?     |

---

## 🎯 Milestone 2: Frontend Integration (Days 5-10)

### Objetivo

Ter React + TypeScript funcionando integrado com backend

### Tasks

#### Task 2.1: Frontend Project Setup ⏱️ 1-2 horas

**Subtasks:**

- [ ] Verify Vite + React installed

  ```bash
  cd leiaute-nfse-ui
  npm list vite react react-dom
  ```

- [ ] Start dev server

  ```bash
  npm run dev
  ```

  **Esperado:** `Local: http://localhost:5173`

- [ ] Install API client

  ```bash
  npm install axios
  # or use built-in fetch
  ```

- [ ] Create environment config
  ```bash
  # .env.local
  VITE_API_URL=http://localhost:8000
  VITE_API_PATH=/api
  ```

---

#### Task 2.2: API Service Layer ⏱️ 2-3 horas

**Arquivo:** `leiaute-nfse-ui/src/services/api.ts`

```typescript
import axios, { AxiosInstance } from "axios";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

class ApiService {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: `${API_BASE_URL}/api`,
      timeout: 10000,
    });

    // Error interceptor
    this.client.interceptors.response.use(
      response => response,
      error => {
        console.error("API Error:", error.response?.data);
        throw error;
      },
    );
  }

  // Services
  async getServices(limit = 10, offset = 0) {
    const { data } = await this.client.get("/services", {
      params: { limit, offset },
    });
    return data;
  }

  async getServiceDetail(id: number) {
    const { data } = await this.client.get(`/services/${id}`);
    return data;
  }

  // Rules
  async getRules(limit = 10, offset = 0, filters = {}) {
    const { data } = await this.client.get("/rules", {
      params: { limit, offset, ...filters },
    });
    return data;
  }

  async getRulesByLevel(level: number, limit = 10) {
    const { data } = await this.client.get(`/rules/filtro/por-nivel/${level}`, {
      params: { limit },
    });
    return data;
  }

  // Search
  async search(query: string) {
    const { data } = await this.client.get("/search", { params: { q: query } });
    return data;
  }
}

export const apiService = new ApiService();
```

**Testes:**

```bash
# Verificar import
import { apiService } from '@services/api'
```

---

#### Task 2.3: TypeScript Models ⏱️ 1-2 horas

**Arquivo:** `leiaute-nfse-ui/src/types/nfse.ts`

```typescript
export interface Servico {
  numero_servico: number;
  nome_servico: string;
  codigo_tributacao: string;
  descricao: string;
}

export interface Regra {
  numero_regra: number;
  servico_id: number;
  campo: string | null;
  regra_negocio: string | null;
  codigo_erro: string | null;
  mensagem_erro: string | null;
  nivel_regra: number | null;
}

export interface Cenario {
  id: number;
  nome_cenario: string;
  descricao: string;
}

export interface CampoLayout {
  id: number;
  caminho_xml: string;
  elemento_xml: string;
  obrigatorio: string;
}

export interface ApiResponse<T> {
  total: number;
  limit: number;
  offset: number;
  items: T[];
}

export interface SearchResult {
  type: "servico" | "regra" | "cenario";
  id: number;
  name: string;
  description: string;
}
```

---

#### Task 2.4: React Components - Básico ⏱️ 3-4 horas

**Componentes a Criar:**

1. **Layout/Header**

   ```tsx
   // src/components/Header.tsx
   export const Header = () => (
     <header className="bg-blue-600 text-white p-4">
       <h1>NFSe Leiaute Portal</h1>
       <p>Busca, Validação e Análise de Regras de NFSe</p>
     </header>
   );
   ```

2. **Services List**

   ```tsx
   // src/components/ServicesList.tsx
   const [services, setServices] = useState<Servico[]>([]);
   const [loading, setLoading] = useState(true);

   useEffect(() => {
     apiService.getServices().then(data => {
       setServices(data.items);
       setLoading(false);
     });
   }, []);

   return (
     <div>
       {loading ? (
         <p>Carregando...</p>
       ) : (
         <ul>
           {services.map(s => (
             <li key={s.numero_servico}>{s.nome_servico}</li>
           ))}
         </ul>
       )}
     </div>
   );
   ```

3. **Rules Filter**

   ```tsx
   // src/components/RulesFilter.tsx
   const [rules, setRules] = useState([]);
   const [nivel, setNivel] = useState<number | null>(null);

   const handleFilter = async (level: number) => {
     setNivel(level);
     const data = await apiService.getRulesByLevel(level);
     setRules(data.items);
   };

   return (
     <div>
       <button onClick={() => handleFilter(1)}>Nível 1</button>
       <button onClick={() => handleFilter(2)}>Nível 2</button>
       <button onClick={() => handleFilter(3)}>Nível 3</button>
       <div>
         {rules.map(r => (
           <div key={r.numero_regra}>
             <h4>{r.numero_regra}</h4>
             <p>{r.mensagem_erro}</p>
           </div>
         ))}
       </div>
     </div>
   );
   ```

**Validação:**

```bash
npm run dev
# Verificar no http://localhost:5173
# - Página carrega
# - Dados aparecem
# - Sem erros de console
```

---

#### Task 2.5: E2E Basic Tests ⏱️ 2-3 horas

**Arquivo:** `leiaute-nfse-ui/e2e/basic.spec.ts` (Playwright)

```typescript
import { test, expect } from "@playwright/test";

test("homepage loads successfully", async ({ page }) => {
  await page.goto("http://localhost:5173");
  await expect(page).toHaveTitle(/NFSe/);
});

test("services list displays data", async ({ page }) => {
  await page.goto("http://localhost:5173");
  await page.click("text=Serviços");
  await page.waitForSelector('[data-testid="service-item"]');
  const items = await page.locator('[data-testid="service-item"]').count();
  expect(items).toBeGreaterThan(0);
});

test("can filter rules by level", async ({ page }) => {
  await page.goto("http://localhost:5173");
  await page.click("text=Regras");
  await page.click('button:has-text("Nível 1")');
  await page.waitForSelector('[data-testid="rule-item"]');
  const level1Rules = await page.locator('[data-testid="rule-item"]').count();
  expect(level1Rules).toBeGreaterThan(0);
});

test("search functionality works", async ({ page }) => {
  await page.goto("http://localhost:5173");
  await page.fill('input[placeholder="Buscar..."]', "nfse");
  await page.press('input[placeholder="Buscar..."]', "Enter");
  await page.waitForSelector('[data-testid="search-result"]');
});

test("api connection verified", async ({ page }) => {
  const apiResponse = await page.request.get("http://localhost:8000/health");
  expect(apiResponse.ok()).toBeTruthy();
});
```

**Rodar:**

```bash
npx playwright test
```

---

### Métricas de Sucesso - Milestone 2

| Métrica                     | Esperado      |
| --------------------------- | ------------- |
| **Frontend loads**          | < 3s          |
| **API calls from browser**  | Success (200) |
| **React components render** | All visible   |
| **E2E tests pass**          | 100%          |

---

## 🎯 Milestone 3: Polish & Testing (Days 10-14)

### Tasks

#### Task 3.1: Performance Optimization ⏱️ 2-3 horas

- [ ] Lazy load routes
- [ ] Add pagination UI
- [ ] Cache API responses
- [ ] Minimize bundle size

#### Task 3.2: Error Handling ⏱️ 1-2 horas

- [ ] Network error UI
- [ ] Timeout handling
- [ ] Validation feedback

#### Task 3.3: Accessibility ⏱️ 2-3 horas

- [ ] ARIA labels
- [ ] Keyboard navigation
- [ ] Color contrast check

#### Task 3.4: CI/CD Setup ⏱️ 2-3 horas

- [ ] GitHub Actions workflow
- [ ] Auto-run tests
- [ ] Build artifacts

---

## 📊 Dependency Tracking

### Backend Dependencies

```
FastAPI==0.104.1 ✅
SQLAlchemy==2.0.23 ✅
Pydantic==2.5.0 ✅
python-multipart==0.0.6 ✅
uvicorn==0.24.0 ✅
pytest==7.4.3 ⏳ (pending)
pytest-cov==4.1.0 ⏳ (pending)
```

### Frontend Dependencies

```
react==18.2.0 ✅
react-dom==18.2.0 ✅
typescript==5.3.3 ✅
vite==5.0.0 ✅
axios==1.6.2 ✅
@playwright/test==1.40.0 ⏳ (pending)
```

---

## 🚀 Critical Path (Minimum Viable Product)

1. ✅ **Data Import** - Completo (328 services, 677 rules)
2. ⏳ **API Validation** - In Progress (3-5 days)
3. ▶️ **Frontend Components** - Ready (5-10 days)
4. ▶️ **E2E Testing** - Ready (10-14 days)
5. ▶️ **MVP Release** - Ready (~14 days)

---

## 📈 Success Metrics

### Quantitativas

- [ ] Server uptime > 99.9%
- [ ] API response time < 200ms (p95)
- [ ] Test coverage > 80%
- [ ] Bundle size < 500KB (gzip)

### Qualitativas

- [ ] No critical bugs in MVP
- [ ] All endpoints documented
- [ ] User flows validated
- [ ] Performance acceptable

---

## 🔄 Feedback Loop

### Weekly Milestones

- Every 7 days: Release mini-milestone
- Code review before merge
- Automated tests must pass
- Documentation updated

### Communication

- Issues tracked in GitHub
- PR reviews within 24h
- Daily standup (async):
  - ✅ Completed yesterday
  - 🏗️ Today's plan
  - 🚧 Blockers

---

## 📚 Additional Resources

- [FastAPI Best Practices](https://fastapi.tiangolo.com/)
- [React Performance](https://react.dev/learn/render-and-commit)
- [Database Design Patterns](https://en.wikipedia.org/wiki/Database_design)
- [Testing Strategies](https://testingpyramid.com/)

---

**Document Version:** 1.0.0  
**Last Updated:** 13 de fevereiro de 2026  
**Next Review Date:** 20 de fevereiro de 2026
