import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db


# Setup: Banco SQLite em memória para testes
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


class TestHealthAndRoot:
    """Testes de health check e root"""
    
    def test_health_check(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"
    
    def test_root(self):
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "titulo" in data
        assert "endpoints" in data


class TestServicosRouter:
    """Testes do router de serviços"""
    
    def test_list_services_empty(self):
        """Testa listagem de serviços vazio"""
        response = client.get("/api/services")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0
        assert data["items"] == []
    
    def test_list_services_pagination(self):
        """Testa paginação de serviços"""
        response = client.get("/api/services?limit=5&offset=0")
        assert response.status_code == 200
        data = response.json()
        assert "total" in data
        assert "limit" in data
        assert data["limit"] == 5
    
    def test_get_service_not_found(self):
        """Testa retorno 404 para serviço inexistente"""
        response = client.get("/api/services/99999")
        assert response.status_code == 404
    
    def test_get_service_rules_not_found(self):
        """Testa retorno 404 para regras de serviço inexistente"""
        response = client.get("/api/services/99999/rules")
        assert response.status_code == 404


class TestRegrasRouter:
    """Testes do router de regras"""
    
    def test_list_rules_empty(self):
        """Testa listagem de regras vazio"""
        response = client.get("/api/rules")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0
        assert data["items"] == []
    
    def test_list_rules_with_filters(self):
        """Testa listagem de regras com filtros"""
        response = client.get("/api/rules?nivel=1&limit=10")
        assert response.status_code == 200
        data = response.json()
        assert data["filtros_aplicados"]["nivel"] == 1
    
    def test_get_rule_not_found(self):
        """Testa retorno 404 para regra inexistente"""
        response = client.get("/api/rules/99999")
        assert response.status_code == 404
    
    def test_get_rules_by_level_invalid(self):
        """Testa nível inválido (deve ser 1-3)"""
        response = client.get("/api/rules/filtro/por-nivel/5")
        assert response.status_code == 422  # Validation error


class TestCenariosRouter:
    """Testes do router de cenários"""
    
    def test_list_scenarios_empty(self):
        """Testa listagem de cenários vazio"""
        response = client.get("/api/scenarios")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0
        assert data["items"] == []
    
    def test_get_scenario_not_found(self):
        """Testa retorno 404 para cenário inexistente"""
        response = client.get("/api/scenarios/99999")
        assert response.status_code == 404
    
    def test_compare_scenarios_empty(self):
        """Testa comparação de cenários vazio"""
        response = client.post("/api/scenarios/compare", 
                             params={"cenarios_ids": [1, 2]})
        assert response.status_code == 404


class TestBuscaRouter:
    """Testes do router de busca"""
    
    def test_search_minimum_length(self):
        """Testa requisição com menos de 2 caracteres"""
        response = client.get("/api/search?q=a")
        assert response.status_code == 422  # Validation error
    
    def test_search_empty_result(self):
        """Testa busca com resultado vazio"""
        response = client.get("/api/search?q=xyz123")
        assert response.status_code == 200
        data = response.json()
        assert data["query"] == "xyz123"
        assert data["total_resultados"] == 0
        assert data["items"] == []
    
    def test_search_by_code_not_found(self):
        """Testa busca por código inexistente"""
        response = client.get("/api/search/codigo/99999")
        assert response.status_code == 200
        assert response.json()["encontrado"] == False
    
    def test_search_by_error_not_found(self):
        """Testa busca por erro inexistente"""
        response = client.get("/api/search/erro/EXXX")
        assert response.status_code == 200
        data = response.json()
        assert data["encontrado"] == False
        assert data["total"] == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
