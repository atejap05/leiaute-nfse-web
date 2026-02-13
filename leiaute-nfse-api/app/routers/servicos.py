from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import ServicoORM, ServicoResponse, ServicoDetail, PaginatedResponse

router = APIRouter(prefix="/api/services", tags=["services"])


@router.get("", response_model=dict)
def list_services(
    limit: int = Query(10, gt=0, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """
    Lista todos os serviços com paginação.
    
    - **limit**: Número de itens por página (padrão: 10, máximo: 100)
    - **offset**: Número de itens para pular (padrão: 0)
    """
    query = db.query(ServicoORM)
    total = query.count()
    
    servicos = query.offset(offset).limit(limit).all()
    
    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "items": [ServicoResponse.model_validate(s) for s in servicos]
    }


@router.get("/{codigo}", response_model=ServicoDetail)
def get_service_detail(codigo: int, db: Session = Depends(get_db)):
    """
    Retorna detalhe de um serviço e suas regras associadas.
    
    - **codigo**: Código de tributação do serviço (ex: 10101)
    """
    servico = db.query(ServicoORM).filter(
        ServicoORM.codigo_tributacao == codigo
    ).first()
    
    if not servico:
        raise HTTPException(status_code=404, detail=f"Serviço {codigo} não encontrado")
    
    return ServicoDetail.model_validate(servico)


@router.get("/{codigo}/rules")
def get_service_rules(codigo: int, db: Session = Depends(get_db)):
    """
    Retorna as regras de validação específicas para um serviço.
    
    - **codigo**: Código de tributação do serviço
    """
    servico = db.query(ServicoORM).filter(
        ServicoORM.codigo_tributacao == codigo
    ).first()
    
    if not servico:
        raise HTTPException(status_code=404, detail=f"Serviço {codigo} não encontrado")
    
    from app.models import RegraResponse
    
    return {
        "codigo_servico": codigo,
        "total_regras": len(servico.regras),
        "regras": [RegraResponse.model_validate(r) for r in servico.regras]
    }
