from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database.config import get_db
from app.database.models import Produto
from app.utils.security import get_current_user
from datetime import datetime




# Rotas de Cadastro de Produtos para o main.py
router = APIRouter()


# Rota para adicionar um produto
@router.post("/cadastro_produto/")
async def adicionar_produto(nome_produto: str,
                            quantidade_estoque: int,
                            descricao_produto: str | None = None,
                            current_user: int = Depends(get_current_user),
                            db: Session = Depends(get_db)
                            ):
    
    # Verificar se o usuario esta autenticado
    if not current_user:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")


    # Verificar se a quantidade de estoque é positiva
    if quantidade_estoque < 0:
        raise HTTPException(status_code=400, detail="A quantidade de estoque não pode ser negativa")
    
    # Tentar adicionar o produto
    try:
        db_produto = Produto(nomeProduto = nome_produto,
                             descricaoProduto = descricao_produto,
                             quantidadeEstoque = quantidade_estoque,
                             dataCriacao = datetime.now(),
                             id_Cliente = current_user
                             )
        
        # Adicionar o produto ao banco de dados
        db.add(db_produto)
        db.commit()
        db.refresh(db_produto)

        # Retornar a mensagem de sucesso e o id do produto
        return {"message": "Produto adicionado com sucesso",
                "id_produto": db_produto.idProduto,
                "next_url": f"/cadastro_produto/fornecedor/{db_produto.idProduto}"}
        

    # Caso ocorra um erro, retornar uma mensagem de erro
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
