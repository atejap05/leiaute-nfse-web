from pydantic_settings import BaseSettings
from functools import lru_cache
from pathlib import Path


class Settings(BaseSettings):
    """Configurações da aplicação"""
    
    # API
    debug: bool = True
    api_title: str = "NFSe Leiaute Portal API"
    api_version: str = "1.0.0"
    api_description: str = "API para consulta do leiaute NFS-e com 328 serviços e 677 regras de validação"
    
    # Database
    database_url: str = "sqlite:///./nfse_leiaute.db"
    
    # Source
    source_dir: str = "../output-source/Leiaute-nfse-rtc-v1-03-00-2013-nt007"
    
    # CORS Configuration
    allowed_origins: str = "*"  # Em produção, separar por vírgula: "https://seudominio.com,https://www.seudominio.com"
    allowed_methods: str = "GET,POST,OPTIONS"
    allowed_headers: str = "Content-Type,Authorization"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Retorna instância única de settings com cache"""
    return Settings()
