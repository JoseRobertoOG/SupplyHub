
from fastapi import APIRouter, HTTPException, Depends
from app.database.models import Produto, Movimentacao
from app.database.config import get_db
from app.utils.security import get_current_user
from sqlalchemy.orm import Session
from app.database.models import TipoMovimentacao
from datetime import datetime

router = APIRouter()


@router.post("/movimentar_produto/{produto_id}")
async def movimentar_produto(
    produto_id: int,
    quantidade: int,
    tipo_movimentacao: TipoMovimentacao,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    try:
        # Verificar se o produto pertence ao cliente atual
        produto = db.query(Produto).filter(
            Produto.idProduto == produto_id,
            Produto.id_Cliente == current_user
        ).first()
        
        if not produto:
            raise HTTPException(status_code=404, detail="Produto não encontrado ou não autorizado")
        
        # Verificar se há estoque suficiente
        if tipo_movimentacao == TipoMovimentacao.ENTRADA:
            produto.quantidadeEstoque += quantidade
        else:
            if produto.quantidadeEstoque < quantidade:
                raise HTTPException(status_code=400, detail="Estoque insuficiente")
            produto.quantidadeEstoque -= quantidade
        
        # Salvar as alterações
        movimentacao = Movimentacao(
            quantidadeMovimentada = quantidade,
            tipoMovimentacao = tipo_movimentacao,
            id_Produto = produto_id,
            dataMovimentacao = datetime.now(),
            id_Cliente = current_user
        )

        db.add(movimentacao)
        db.commit()
        db.refresh(movimentacao)

        return {"message": "Movimentação realizada com sucesso"}
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
        