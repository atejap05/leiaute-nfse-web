from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from typing import Optional, List
from app.database import get_db
from app.models import RegraORM, RegraResponse, PaginatedRegras, FilteredRulesResponse, FilteredRulesByErrorResponse

router = APIRouter(prefix="/api/rules", tags=["rules"])


@router.get("", response_model=PaginatedRegras)
def list_rules(
    limit: int = Query(10, gt=0, le=100),
    offset: int = Query(0, ge=0),
    nivel: Optional[int] = Query(None, ge=1, le=3),
    codigo_erro: Optional[str] = Query(None),
    campo: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Lista regras de validação com filtros opcionais.
    
    - **limit**: Número de itens por página (máximo: 100)
    - **offset**: Número de itens para pular
    - **nivel**: Filtro por nível (1, 2 ou 3)
    - **codigo_erro**: Filtro por código de erro (ex: E1260)
    - **campo**: Filtro por nome do campo
    """
    query = db.query(RegraORM)
    
    if nivel is not None:
        query = query.filter(RegraORM.nivel_regra == nivel)
    
    if codigo_erro:
        query = query.filter(RegraORM.codigo_erro.contains(codigo_erro))
    
    if campo:
        query = query.filter(RegraORM.campo.contains(campo))
    
    total = query.count()
    regras = query.offset(offset).limit(limit).all()
    
    return PaginatedRegras(
        total=total,
        limit=limit,
        offset=offset,
        filtros_aplicados={
            "nivel": nivel,
            "codigo_erro": codigo_erro,
            "campo": campo
        },
        items=[RegraResponse.model_validate(r) for r in regras]
    )


@router.get("/{numero}", response_model=RegraResponse)
def get_rule_detail(numero: int, db: Session = Depends(get_db)):
    """
    Retorna detalhe de uma regra específica.
    
    - **numero**: Número da regra
    """
    regra = db.query(RegraORM).filter(
        RegraORM.numero_regra == numero
    ).first()
    
    if not regra:
        raise HTTPException(status_code=404, detail=f"Regra {numero} não encontrada")
    
    return RegraResponse.model_validate(regra)


@router.get("/filtro/por-nivel/{nivel}", response_model=FilteredRulesResponse)
def get_rules_by_level(
    nivel: int = Path(..., ge=1, le=3),
    limit: int = Query(20, gt=0, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """
    Retorna regras filtradas por nível (1, 2 ou 3).
    """
    query = db.query(RegraORM).filter(RegraORM.nivel_regra == nivel)
    total = query.count()
    
    regras = query.offset(offset).limit(limit).all()
    
    return FilteredRulesResponse(
        nivel=nivel,
        total=total,
        limit=limit,
        offset=offset,
        items=[RegraResponse.model_validate(r) for r in regras]
    )


@router.get("/filtro/por-erro/{codigo_erro}", response_model=FilteredRulesByErrorResponse)
def get_rules_by_error_code(
    codigo_erro: str,
    db: Session = Depends(get_db)
):
    """
    Retorna todas as regras com um código de erro específico.
    
    - **codigo_erro**: Código de erro (ex: E1260)
    """
    regras = db.query(RegraORM).filter(
        RegraORM.codigo_erro == codigo_erro
    ).all()
    
    if not regras:
        raise HTTPException(status_code=404, detail=f"Nenhuma regra encontrada para erro {codigo_erro}")
    
    return FilteredRulesByErrorResponse(
        codigo_erro=codigo_erro,
        total=len(regras),
        limit=len(regras),
        offset=0,
        items=[RegraResponse.model_validate(r) for r in regras]
    )
