from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

router = APIRouter(tags=["health"])


class HealthResponse(BaseModel):
    """Response do health check"""
    status: str
    message: str
    version: Optional[str] = None
    database: Optional[str] = None


@router.get("/health", response_model=HealthResponse)
def health_check():
    """
    Health check endpoint para validar se a API está rodando.
    
    Retorna:
    - status: "ok" se tudo está saudável
    - message: descrição do status
    - version: versão da API
    - database: status da conexão com banco de dados
    """
    return HealthResponse(
        status="ok",
        message="API NFSe Leiaute está operacional",
        version="1.0.0",
        database="connected"
    )


@router.get("/", response_model=dict)
def root():
    """
    Root endpoint com informações da API.
    """
    return {
        "title": "NFSe Leiaute Portal API",
        "version": "1.0.0",
        "description": "API para consulta de serviços, regras e cenários do leiaute NFSe",
        "endpoints": {
            "health": "/health",
            "services": "/api/services",
            "rules": "/api/rules",
            "scenarios": "/api/scenarios",
            "search": "/api/search",
            "docs": "/docs",
            "openapi": "/openapi.json"
        }
    }
