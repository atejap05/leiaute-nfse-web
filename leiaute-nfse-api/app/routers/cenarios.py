from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from app.database import get_db
from app.models import CenarioORM, CenarioResponse, PaginatedCenarios, ScenarioComparison, DomesticScenariosResponse, ExportScenariosResponse

router = APIRouter(prefix="/api/scenarios", tags=["scenarios"])


@router.get("", response_model=PaginatedCenarios)
def list_scenarios(
    limit: int = Query(10, gt=0, le=100),
    offset: int = Query(0, ge=0),
    endereco_tomador: Optional[str] = Query(None),
    local_prestacao: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Lista cenários de exportação com filtros opcionais.
    
    - **limit**: Número de itens por página
    - **offset**: Número de itens para pular
    - **endereco_tomador**: Filtrar por endereço do tomador (Brasil/Exterior)
    - **local_prestacao**: Filtrar por local de prestação (Brasil/Exterior)
    """
    query = db.query(CenarioORM)
    
    if endereco_tomador:
        query = query.filter(CenarioORM.endereco_tomador.contains(endereco_tomador))
    
    if local_prestacao:
        query = query.filter(CenarioORM.local_prestacao.contains(local_prestacao))
    
    total = query.count()
    cenarios = query.offset(offset).limit(limit).all()
    
    return PaginatedCenarios(
        total=total,
        limit=limit,
        offset=offset,
        filtros_aplicados={
            "endereco_tomador": endereco_tomador,
            "local_prestacao": local_prestacao
        },
        items=[CenarioResponse.model_validate(c) for c in cenarios]
    )


@router.get("/{numero}", response_model=CenarioResponse)
def get_scenario_detail(numero: int, db: Session = Depends(get_db)):
    """
    Retorna detalhe de um cenário específico.
    
    - **numero**: Número do cenário
    """
    cenario = db.query(CenarioORM).filter(
        CenarioORM.numero_cenario == numero
    ).first()
    
    if not cenario:
        raise HTTPException(status_code=404, detail=f"Cenário {numero} não encontrado")
    
    return CenarioResponse.model_validate(cenario)


@router.post("/compare", response_model=ScenarioComparison)
def compare_scenarios(
    cenarios_ids: List[int] = Query(..., min_items=2, max_items=5),
    db: Session = Depends(get_db)
):
    """
    Compara múltiplos cenários lado a lado.
    
    - **cenarios_ids**: IDs dos cenários a comparar (2-5 cenários)
    
    Exemplo: POST /api/scenarios/compare?cenarios_ids=1&cenarios_ids=2&cenarios_ids=3
    """
    cenarios = db.query(CenarioORM).filter(
        CenarioORM.numero_cenario.in_(cenarios_ids)
    ).all()
    
    if len(cenarios) < len(cenarios_ids):
        raise HTTPException(status_code=404, detail="Um ou mais cenários não encontrados")
    
    diferencas = _extract_differences(cenarios)
    
    return ScenarioComparison(
        cenarios_comparados=cenarios_ids,
        total_campos=6,
        diferencas_encontradas=len(diferencas),
        valores_encontrados=diferencas
    )


def _extract_differences(cenarios: List[CenarioORM]) -> dict:
    """Helper para extrair diferenças entre cenários"""
    if not cenarios:
        return {}
    
    campos_diferentes = {}
    primeiro = cenarios[0]
    
    campos_chave = [
        'endereco_tomador',
        'endereco_intermediario',
        'local_prestacao',
        'tributacao_issqn',
        'obrigatorio_nbs',
        'obrigatorio_pais_resultado'
    ]
    
    for campo in campos_chave:
        valores = set()
        for c in cenarios:
            valor = getattr(c, campo)
            valores.add(str(valor))
        
        if len(valores) > 1:
            campos_diferentes[campo] = {
                "valores_encontrados": list(valores),
                "diferem": True
            }
    
    return campos_diferentes


@router.get("/filtro/brasil-brasil", response_model=DomesticScenariosResponse)
def get_domestic_scenarios(
    limit: int = Query(10, gt=0, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """
    Retorna cenários onde prestador e tomador estão no Brasil.
    """
    cenarios = db.query(CenarioORM).filter(
        CenarioORM.endereco_tomador == "Brasil",
        CenarioORM.local_prestacao == "Brasil"
    ).offset(offset).limit(limit).all()
    
    total = db.query(CenarioORM).filter(
        CenarioORM.endereco_tomador == "Brasil",
        CenarioORM.local_prestacao == "Brasil"
    ).count()
    
    return DomesticScenariosResponse(
        total=total,
        limit=limit,
        offset=offset,
        items=[CenarioResponse.model_validate(c) for c in cenarios]
    )


@router.get("/filtro/exportacao", response_model=ExportScenariosResponse)
def get_export_scenarios(
    limit: int = Query(10, gt=0, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """
    Retorna cenários de exportação (tomador ou prestador no exterior).
    """
    cenarios = db.query(CenarioORM).filter(
        (CenarioORM.endereco_tomador == "Exterior") |
        (CenarioORM.local_prestacao == "Exterior")
    ).offset(offset).limit(limit).all()
    
    total = db.query(CenarioORM).filter(
        (CenarioORM.endereco_tomador == "Exterior") |
        (CenarioORM.local_prestacao == "Exterior")
    ).count()
    
    return ExportScenariosResponse(
        total=total,
        limit=limit,
        offset=offset,
        items=[CenarioResponse.model_validate(c) for c in cenarios]
    )
