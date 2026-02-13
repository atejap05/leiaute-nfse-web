from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models import ServicoORM, RegraORM, CampoLayoutORM, SearchResult

router = APIRouter(prefix="/api/search", tags=["search"])


@router.get("", response_model=dict)
def search(
    q: str = Query(..., min_length=2, max_length=255),
    tipo: Optional[str] = Query(None, description="Filtro por tipo: servico, regra, campo"),
    limit: int = Query(20, gt=0, le=100),
    db: Session = Depends(get_db)
):
    """
    Busca unificada em serviços, regras e campos de leiaute.
    
    - **q**: Texto a buscar (mínimo 2 caracteres)
    - **tipo**: Filtrar por tipo (servico, regra, campo) - opcional
    - **limit**: Número máximo de resultados
    
    Exemplos:
    - `?q=análise` - busca em descrições de serviços
    - `?q=E1260` - busca por código de erro
    - `?q=versao&tipo=regra` - busca no campo "regra_negocio"
    """
    resultados = []
    query_lower = q.lower()
    
    # Busca em Serviços
    if tipo is None or tipo == "servico":
        servicos = db.query(ServicoORM).filter(
            (ServicoORM.descricao.ilike(f"%{q}%")) |
            (ServicoORM.codigo_tributacao == int(q) if q.isdigit() else False)
        ).limit(limit).all()
        
        for s in servicos:
            score = 1.0 if q.isdigit() and int(q) == s.codigo_tributacao else 0.8
            resultados.append({
                "tipo": "servico",
                "match_score": score,
                "codigo": s.codigo_tributacao,
                "descricao": s.descricao,
                "id": s.id
            })
    
    # Busca em Regras
    if tipo is None or tipo == "regra":
        regras = db.query(RegraORM).filter(
            (RegraORM.regra_negocio.ilike(f"%{q}%")) |
            (RegraORM.codigo_erro.contains(q)) |
            (RegraORM.campo.ilike(f"%{q}%")) |
            (RegraORM.numero_regra == int(q) if q.isdigit() else False)
        ).limit(limit).all()
        
        for r in regras:
            # Score mais alto se encontra no código de erro
            if r.codigo_erro.contains(q):
                score = 1.0
            elif q.isdigit() and r.numero_regra == int(q):
                score = 1.0
            else:
                score = 0.7
            
            resultados.append({
                "tipo": "regra",
                "match_score": score,
                "numero": r.numero_regra,
                "codigo_erro": r.codigo_erro,
                "campo": r.campo,
                "descricao": r.regra_negocio,
                "nivel": r.nivel_regra,
                "id": r.id
            })
    
    # Busca em Campos do Leiaute
    if tipo is None or tipo == "campo":
        campos = db.query(CampoLayoutORM).filter(
            (CampoLayoutORM.descricao.ilike(f"%{q}%")) |
            (CampoLayoutORM.nome_campo.ilike(f"%{q}%")) |
            (CampoLayoutORM.elemento_xml.ilike(f"%{q}%")) |
            (CampoLayoutORM.número_campo == int(q) if q.isdigit() else False)
        ).limit(limit).all()
        
        for c in campos:
            score = 1.0 if q.isdigit() and c.numero_campo == int(q) else 0.75
            resultados.append({
                "tipo": "campo",
                "match_score": score,
                "numero": c.numero_campo,
                "nome": c.nome_campo,
                "elemento_xml": c.elemento_xml,
                "descricao": c.descricao,
                "id": c.id
            })
    
    # Ordena por score descendente
    resultados.sort(key=lambda x: x["match_score"], reverse=True)
    resultados = resultados[:limit]
    
    return {
        "query": q,
        "filtro_tipo": tipo,
        "total_resultados": len(resultados),
        "items": resultados
    }


@router.get("/codigo/{codigo}", response_model=dict)
def search_by_service_code(codigo: int, db: Session = Depends(get_db)):
    """
    Busca um serviço pelo código de tributação.
    
    - **codigo**: Código de tributação (ex: 10101)
    """
    servico = db.query(ServicoORM).filter(
        ServicoORM.codigo_tributacao == codigo
    ).first()
    
    if not servico:
        return {"encontrado": False, "mensagem": f"Serviço {codigo} não encontrado"}
    
    return {
        "encontrado": True,
        "servico": {
            "codigo": servico.codigo_tributacao,
            "descricao": servico.descricao,
            "localidade_incidencia": {
                "estabelecimento_prestador": servico.estabelecimento_prestador,
                "local_prestacao": servico.local_prestacao,
                "estabelecimento_tomador": servico.estabelecimento_tomador,
                "estabelecimento_emitente": servico.estabelecimento_emitente
            }
        }
    }


@router.get("/erro/{codigo_erro}", response_model=dict)
def search_by_error_code(codigo_erro: str, db: Session = Depends(get_db)):
    """
    Busca regras por código de erro.
    
    - **codigo_erro**: Código identificador do erro (ex: E1260)
    """
    regras = db.query(RegraORM).filter(
        RegraORM.codigo_erro == codigo_erro
    ).all()
    
    if not regras:
        return {
            "encontrado": False,
            "codigo_erro": codigo_erro,
            "total": 0,
            "regras": []
        }
    
    return {
        "encontrado": True,
        "codigo_erro": codigo_erro,
        "total": len(regras),
        "regras": [
            {
                "numero": r.numero_regra,
                "campo": r.campo,
                "descricao": r.regra_negocio,
                "mensagem_erro": r.mensagem_erro,
                "nivel": r.nivel_regra
            }
            for r in regras
        ]
    }
