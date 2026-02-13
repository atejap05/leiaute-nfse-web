from __future__ import annotations
from sqlalchemy import Column, Integer, String, Text, Index, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from typing import Optional, List
from app.database import Base


# ============================================================================
# MODELOS SQLALCHEMY (ORM) - para banco de dados
# ============================================================================

class ServicoORM(Base):
    """Tabela de serviços (328 serviços de incidência)"""
    __tablename__ = "servicos"
    
    id = Column(Integer, primary_key=True, index=True)
    codigo_tributacao = Column(Integer, unique=True, nullable=False, index=True)
    descricao = Column(Text, nullable=False)
    
    # Localidade de Incidência (LC 116/03)
    estabelecimento_prestador = Column(String(1), nullable=True)  # "X"
    local_prestacao = Column(String(1), nullable=True)  # "X"
    estabelecimento_tomador = Column(String(1), nullable=True)  # "X"
    estabelecimento_emitente = Column(String(1), nullable=True)  # "X"
    
    # Grupos de Informação
    obrigatorio = Column(String(1), nullable=True)  # "-" ou "X"
    info_complementares = Column(String(1), nullable=True)  # "-" ou "X"
    
    versao_leiaute = Column(String(50), nullable=False)
    
    # Relationships
    regras = relationship("RegraORM", back_populates="servico", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index('idx_servicos_codigo', 'codigo_tributacao'),
        Index('idx_servicos_versao', 'versao_leiaute'),
    )


class RegraORM(Base):
    """Tabela de regras de validação (677 regras)"""
    __tablename__ = "regras"
    
    id = Column(Integer, primary_key=True, index=True)
    numero_regra = Column(Integer, nullable=False, index=True)
    campo = Column(String(255), nullable=True)
    regra_negocio = Column(Text, nullable=True)
    codigo_erro = Column(String(10), nullable=True, index=True)  # E1260, E1263, etc
    mensagem_erro = Column(Text, nullable=True)
    nivel_regra = Column(Integer, nullable=True, index=True)  # 1, 2 ou 3
    contexto = Column(String(255), nullable=True)  # "Emissores públicos", "ADN", etc
    exemplay = Column(Text, nullable=True)
    
    # Foreign key
    servico_id = Column(Integer, ForeignKey("servicos.id"), nullable=True, index=True)
    servico = relationship("ServicoORM", back_populates="regras")
    
    versao_leiaute = Column(String(50), nullable=False)
    
    __table_args__ = (
        Index('idx_regras_numero', 'numero_regra'),
        Index('idx_regras_codigo_erro', 'codigo_erro'),
        Index('idx_regras_nivel', 'nivel_regra'),
        Index('idx_regras_campo', 'campo'),
        Index('idx_regras_servico_nivel', 'servico_id', 'nivel_regra'),
    )


class CenarioORM(Base):
    """Tabela de cenários de exportação (112 cenários)"""
    __tablename__ = "cenarios"
    
    id = Column(Integer, primary_key=True, index=True)
    numero_cenario = Column(Integer, unique=True, nullable=False, index=True)
    
    # Localidades
    endereco_tomador = Column(String(50), nullable=False)  # "Brasil", "Exterior"
    endereco_intermediario = Column(String(50), nullable=False)
    local_prestacao = Column(String(50), nullable=False)
    
    # Tributação
    imunidade_exportacao = Column(String(255), nullable=True)
    tributacao_issqn = Column(String(50), nullable=True)
    
    # Comex
    obrigatorio_nbs = Column(Boolean, default=False)
    obrigatorio_pais_resultado = Column(Boolean, default=False)
    descricao = Column(Text, nullable=True)
    
    versao_leiaute = Column(String(50), nullable=False)
    
    __table_args__ = (
        Index('idx_cenarios_numero', 'numero_cenario'),
        Index('idx_cenarios_localidades', 'endereco_tomador', 'local_prestacao'),
    )


class CampoLayoutORM(Base):
    """Tabela de campos do leiaute XML (431 campos)"""
    __tablename__ = "campos_layout"
    
    id = Column(Integer, primary_key=True, index=True)
    numero_campo = Column(Integer, nullable=False, index=True)
    
    caminho_xml = Column(String(255), nullable=False, index=True)  # "NFSe/infNFSe/"
    nome_campo = Column(String(255), nullable=False)
    elemento_xml = Column(String(100), nullable=False)
    
    tipo_dado = Column(String(1), nullable=False)  # C, N, D, ID, etc
    ocorrencia = Column(String(10), nullable=False)  # "1-1", "0-1", "1-N", "0-N"
    tamanho_maximo = Column(Integer, nullable=True)
    
    descricao = Column(Text, nullable=False)
    observacoes = Column(Text, nullable=True)
    
    versao_leiaute = Column(String(50), nullable=False)
    
    campos_restritivos = relationship(
        "RestricaoORM", 
        back_populates="campo", 
        cascade="all, delete-orphan"
    )
    
    __table_args__ = (
        Index('idx_campos_numero', 'numero_campo'),
        Index('idx_campos_xml_path', 'caminho_xml'),
        Index('idx_campos_elemento', 'elemento_xml'),
    )


class RestricaoORM(Base):
    """Restrições e valores permitidos para campos"""
    __tablename__ = "restricoes"
    
    id = Column(Integer, primary_key=True, index=True)
    campo_id = Column(Integer, ForeignKey("campos_layout.id"), nullable=False)
    campo = relationship("CampoLayoutORM", back_populates="campos_restritivos")
    
    tipo_restricao = Column(String(50), nullable=False)  # "lista_valores", "intervalo", "pattern"
    descricao = Column(Text, nullable=False)
    
    versao_leiaute = Column(String(50), nullable=False)


class MasterIndexORM(Base):
    """Índice master com metadados da versão"""
    __tablename__ = "master_index"
    
    id = Column(Integer, primary_key=True, index=True)
    versao_leiaute = Column(String(50), unique=True, nullable=False)
    arquivo_origem = Column(String(255), nullable=False)
    data_conversao = Column(String(50), nullable=False)
    
    total_servicos = Column(Integer, nullable=False)
    total_regras = Column(Integer, nullable=False)
    total_cenarios = Column(Integer, nullable=False)
    total_campos = Column(Integer, nullable=False)
    total_restricoes = Column(Integer, nullable=False)
    
    documentacao = Column(Text, nullable=True)


# ============================================================================
# MODELOS PYDANTIC (API Request/Response) - para serialização JSON
# ============================================================================

class ServicoBase(BaseModel):
    """Schema base para Serviço"""
    codigo_tributacao: int
    descricao: str
    estabelecimento_prestador: Optional[str] = None
    local_prestacao: Optional[str] = None
    estabelecimento_tomador: Optional[str] = None
    estabelecimento_emitente: Optional[str] = None
    obrigatorio: Optional[str] = None
    info_complementares: Optional[str] = None


class ServicoCreate(ServicoBase):
    """Schema para criar Serviço"""
    versao_leiaute: str


class ServicoResponse(ServicoBase):
    """Schema de resposta para Serviço"""
    id: int
    versao_leiaute: str
    
    class Config:
        from_attributes = True


class ServicoDetail(ServicoResponse):
    """Detalhe de serviço com regras associadas"""
    regras_aplicaveis: List['RegraResponse'] = []
    
    class Config:
        from_attributes = True


# ============================================================================

class RegraBase(BaseModel):
    """Schema base para Regra"""
    numero_regra: int
    campo: Optional[str] = None
    regra_negocio: Optional[str] = None
    codigo_erro: Optional[str] = None
    mensagem_erro: Optional[str] = None
    nivel_regra: Optional[int] = None
    contexto: Optional[str] = None
    exemplay: Optional[str] = None


class RegraCreate(RegraBase):
    """Schema para criar Regra"""
    versao_leiaute: str


class RegraResponse(RegraBase):
    """Schema de resposta para Regra"""
    id: int
    servico_id: Optional[int] = None
    versao_leiaute: str
    
    class Config:
        from_attributes = True


# ============================================================================

class CenarioBase(BaseModel):
    """Schema base para Cenário"""
    numero_cenario: int
    endereco_tomador: str
    endereco_intermediario: str
    local_prestacao: str
    imunidade_exportacao: Optional[str] = None
    tributacao_issqn: Optional[str] = None
    obrigatorio_nbs: bool = False
    obrigatorio_pais_resultado: bool = False
    descricao: Optional[str] = None


class CenarioCreate(CenarioBase):
    """Schema para criar Cenário"""
    versao_leiaute: str


class CenarioResponse(CenarioBase):
    """Schema de resposta para Cenário"""
    id: int
    versao_leiaute: str
    
    class Config:
        from_attributes = True


# ============================================================================

class RestricaoResponse(BaseModel):
    """Schema de resposta para Restrição"""
    id: int
    tipo_restricao: str
    descricao: str
    versao_leiaute: str
    
    class Config:
        from_attributes = True


class CampoLayoutBase(BaseModel):
    """Schema base para Campo Layout"""
    numero_campo: int
    caminho_xml: str
    nome_campo: str
    elemento_xml: str
    tipo_dado: str
    ocorrencia: str
    tamanho_maximo: Optional[int] = None
    descricao: str
    observacoes: Optional[str] = None


class CampoLayoutCreate(CampoLayoutBase):
    """Schema para criar Campo Layout"""
    versao_leiaute: str


class CampoLayoutResponse(CampoLayoutBase):
    """Schema de resposta para Campo Layout"""
    id: int
    versao_leiaute: str
    campos_restritivos: List[RestricaoResponse] = []
    
    class Config:
        from_attributes = True


# ============================================================================

class MasterIndexResponse(BaseModel):
    """Schema de resposta para Master Index"""
    id: int
    versao_leiaute: str
    arquivo_origem: str
    data_conversao: str
    total_servicos: int
    total_regras: int
    total_cenarios: int
    total_campos: int
    total_restricoes: int
    documentacao: Optional[str] = None
    
    class Config:
        from_attributes = True


# ============================================================================
# Pagination Schema
# ============================================================================

class PaginationParams(BaseModel):
    """Parâmetros de paginação"""
    limit: int = 10
    offset: int = 0
    
    class Config:
        ge = 1  # limit >= 1


class PaginatedResponse(BaseModel):
    """Response genérico com paginação"""
    total: int
    limit: int
    offset: int
    items: list


# ============================================================================
# Search Schema
# ============================================================================

class SearchResult(BaseModel):
    """Resultado de busca unificada"""
    tipo: str  # "servico", "regra", "campo"
    match_score: float  # 0.0 a 1.0
    dados: dict


class SearchResponse(BaseModel):
    """Response de busca com paginação"""
    query: str
    total_resultados: int
    resultados: List[SearchResult]


# Rebuild models that use forward references
ServicoDetail.model_rebuild()
