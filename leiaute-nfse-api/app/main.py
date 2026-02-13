from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.config import get_settings
from app.database import init_db
from app.routers import servicos, regras, cenarios, busca

# ============================================================================
# Inicialização
# ============================================================================

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle events para a aplicação FastAPI.
    Inicializa banco de dados na startup.
    """
    # Startup
    print("🚀 Iniciando aplicação NFSe API...")
    init_db()
    print("✅ Banco de dados inicializado")
    
    yield
    
    # Shutdown
    print("🛑 Encerrando aplicação...")


# ============================================================================
# Criação da aplicação
# ============================================================================

app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version,
    lifespan=lifespan,
)


# ============================================================================
# CORS (Para permitir requisições do React)
# ============================================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.debug else ["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# Routers
# ============================================================================

app.include_router(servicos.router)
app.include_router(regras.router)
app.include_router(cenarios.router)
app.include_router(busca.router)


# ============================================================================
# Health Check
# ============================================================================

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "version": settings.api_version,
        "api_title": settings.api_title
    }


@app.get("/")
def root():
    """Root endpoint com informações da API"""
    return {
        "titulo": settings.api_title,
        "descricao": settings.api_description,
        "versao": settings.api_version,
        "endpoints": {
            "docs": "/docs",
            "healthcheck": "/health",
            "servicos": "/api/services",
            "regras": "/api/rules",
            "cenarios": "/api/scenarios",
            "busca": "/api/search"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )
