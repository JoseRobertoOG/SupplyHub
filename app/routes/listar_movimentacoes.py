from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database.config import get_db
from app.database.models import Movimentacao, Produto
from app.utils.security import get_current_user
from typing import List
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

# Modelo de resposta
class MovimentacaoResponse(BaseModel):
    nome_produto: str
    quantidade: int
    tipo: str
    data: str

@router.get("/movimentacoes/", response_model=List[MovimentacaoResponse])
@router.get("/movimentacoes/{produto_id}", response_model=List[MovimentacaoResponse])
async def listar_movimentacoes(
    produto_id: int | None = None,
    current_user: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Lista todas as movimentações de produtos do cliente.
    Se produto_id for fornecido, filtra apenas as movimentações daquele produto.
    """
    try:
        # Se produto_id foi fornecido, verifica se o produto pertence ao usuário
        if produto_id:
            produto = db.query(Produto).filter(
                Produto.idProduto == produto_id,
                Produto.id_Cliente == current_user
            ).first()
            
            if not produto:
                raise HTTPException(
                    status_code=404,
                    detail="Produto não encontrado ou não autorizado"
                )

        # Consulta base com join em Produto
        query = db.query(Movimentacao, Produto.nomeProduto)\
                 .join(Produto, Movimentacao.id_Produto == Produto.idProduto)\
                 .filter(
                     Movimentacao.id_Cliente == current_user,
                     Produto.id_Cliente == current_user  # Garante que só retorna produtos do usuário
                 )

        # Adiciona filtro por produto se especificado
        if produto_id:
            query = query.filter(Movimentacao.id_Produto == produto_id)

        # Executa a consulta
        resultados = query.all()

        # Formata os resultados
        movimentacoes_formatadas = [
            MovimentacaoResponse(
                nome_produto=resultado[1],
                quantidade=resultado[0].quantidadeMovimentada,
                tipo=resultado[0].tipoMovimentacao.value,
                data=resultado[0].dataMovimentacao.strftime("%d/%m/%Y %H:%M:%S")
            )
            for resultado in resultados
        ]

        return movimentacoes_formatadas

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao listar movimentações: {str(e)}"
        )