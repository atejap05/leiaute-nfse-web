import json
import logging
import time
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from contextlib import asynccontextmanager
from app.config import get_settings
from app.database import init_db
from app.routers import servicos, regras, cenarios, busca, health

# ============================================================================
# Inicialização
# ============================================================================

settings = get_settings()
logger = logging.getLogger("nfse_api")
if not logger.handlers:
    logging.basicConfig(level=logging.INFO)
logger.setLevel(logging.INFO)


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _log_event(level: int, event: str, **fields: Any) -> None:
    payload = {"event": event, "timestamp": _utc_now(), **fields}
    logger.log(level, json.dumps(payload, ensure_ascii=False))


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle events para a aplicação FastAPI.
    Inicializa banco de dados na startup.
    """
    # Startup
    _log_event(logging.INFO, "app_startup", message="Iniciando aplicação NFSe API")
    init_db()
    _log_event(logging.INFO, "db_initialized", message="Banco de dados inicializado")
    
    yield
    
    # Shutdown
    _log_event(logging.INFO, "app_shutdown", message="Encerrando aplicação")


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

# Parse allowed origins
if settings.allowed_origins == "*" or settings.debug:
    cors_origins = ["*"]
else:
    # Split por vírgula se houver múltiplos domínios
    cors_origins = [origin.strip() for origin in settings.allowed_origins.split(",")]

# Parse allowed methods
cors_methods = [method.strip() for method in settings.allowed_methods.split(",")]

# Parse allowed headers
cors_headers = [header.strip() for header in settings.allowed_headers.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=cors_methods,
    allow_headers=cors_headers,
)


# ============================================================================
# Logging middleware
# ============================================================================

@app.middleware("http")
async def structured_logging_middleware(request: Request, call_next):
    start = time.perf_counter()
    request_id = request.headers.get("X-Request-ID") or str(uuid4())
    request.state.request_id = request_id

    try:
        response = await call_next(request)
        duration_ms = round((time.perf_counter() - start) * 1000, 2)

        _log_event(
            logging.INFO,
            "http_request",
            request_id=request_id,
            method=request.method,
            path=str(request.url.path),
            query=str(request.url.query),
            status_code=response.status_code,
            duration_ms=duration_ms,
            client_ip=request.client.host if request.client else None,
        )

        response.headers["X-Request-ID"] = request_id
        return response
    except Exception:
        duration_ms = round((time.perf_counter() - start) * 1000, 2)
        _log_event(
            logging.ERROR,
            "http_request_exception",
            request_id=request_id,
            method=request.method,
            path=str(request.url.path),
            duration_ms=duration_ms,
            client_ip=request.client.host if request.client else None,
        )
        raise


# ============================================================================
# Error handlers globais
# ============================================================================

def _error_payload(
    code: str,
    message: str,
    status_code: int,
    path: str | None = None,
    request_id: str | None = None,
    details: list[dict] | None = None,
) -> dict:
    payload = {
        "error": {
            "code": code,
            "message": message,
            "status_code": status_code,
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        }
    }

    if path is not None:
        payload["error"]["path"] = path

    if request_id is not None:
        payload["error"]["request_id"] = request_id

    if details:
        payload["error"]["details"] = details

    return payload


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    code_map = {
        400: "E400",
        401: "E401",
        403: "E403",
        404: "E404",
        405: "E405",
        409: "E409",
    }

    request_id = getattr(request.state, "request_id", None)
    _log_event(
        logging.WARNING if exc.status_code < 500 else logging.ERROR,
        "http_error",
        request_id=request_id,
        method=request.method,
        path=str(request.url.path),
        status_code=exc.status_code,
        code=code_map.get(exc.status_code, f"E{exc.status_code}"),
        message=str(exc.detail),
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=_error_payload(
            code=code_map.get(exc.status_code, f"E{exc.status_code}"),
            message=str(exc.detail),
            status_code=exc.status_code,
            path=str(request.url.path),
            request_id=request_id,
        ),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    request_id = getattr(request.state, "request_id", None)
    _log_event(
        logging.WARNING,
        "validation_error",
        request_id=request_id,
        method=request.method,
        path=str(request.url.path),
        status_code=422,
        errors_count=len(exc.errors()),
    )

    return JSONResponse(
        status_code=422,
        content=_error_payload(
            code="E422",
            message="Validation error",
            status_code=422,
            path=str(request.url.path),
            request_id=request_id,
            details=exc.errors(),
        ),
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    request_id = getattr(request.state, "request_id", None)
    logger.exception(
        json.dumps(
            {
                "event": "unhandled_exception",
                "timestamp": _utc_now(),
                "request_id": request_id,
                "method": request.method,
                "path": str(request.url.path),
                "message": str(exc),
            },
            ensure_ascii=False,
        )
    )

    return JSONResponse(
        status_code=500,
        content=_error_payload(
            code="E500",
            message="Internal server error",
            status_code=500,
            path=str(request.url.path),
            request_id=request_id,
        ),
    )


# ============================================================================
# Routers
# ============================================================================

app.include_router(health.router)
app.include_router(servicos.router)
app.include_router(regras.router)
app.include_router(cenarios.router)
app.include_router(busca.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )
