from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session, joinedload
from app.database.config import get_db
from app.database.models import Produto, Fornecedor, TelefoneFornecedor, FornecedorProduto
from app.utils.security import get_current_user
from typing import List
from pydantic import BaseModel

router = APIRouter()

class TelefoneResponse(BaseModel):
    numero: str
    tipo: str

    class Config:
        from_attributes = True

class FornecedorResponse(BaseModel):
    id: int
    nome: str
    email: str
    telefones: List[TelefoneResponse]
    preco_produto: float

    class Config:
        from_attributes = True

class ProdutoResponse(BaseModel):
    id: int
    nome: str
    descricao: str
    quantidade_estoque: int
    fornecedores: List[FornecedorResponse]

    class Config:
        from_attributes = True

@router.get("/produtos/", 
    response_model=List[ProdutoResponse],
    summary="Listar produtos do usuário",
    description="Retorna todos os produtos do usuário com seus fornecedores e detalhes"
)
async def listar_produtos(
    current_user: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        # Buscar produtos do usuário com relacionamentos
        produtos = db.query(Produto).filter(
            Produto.id_Cliente == current_user
        ).all()

        resultado = []
        for produto in produtos:
            # Buscar fornecedores e seus detalhes para cada produto
            fornecedores_produto = db.query(
                Fornecedor,
                FornecedorProduto.precoFornecedorProduto
            ).join(
                FornecedorProduto,
                Fornecedor.idFornecedor == FornecedorProduto.id_Fornecedor
            ).filter(
                FornecedorProduto.id_Produto == produto.idProduto
            ).all()

            fornecedores_lista = []
            for fornecedor, preco in fornecedores_produto:
                # Buscar telefones do fornecedor
                telefones = db.query(TelefoneFornecedor).filter(
                    TelefoneFornecedor.id_Fornecedor == fornecedor.idFornecedor
                ).all()

                fornecedores_lista.append({
                    "id": fornecedor.idFornecedor,
                    "nome": fornecedor.nomeFornecedor,
                    "email": fornecedor.emailFornecedor,
                    "telefones": [
                        {
                            "numero": tel.numeroTelefoneFornecedor,
                            "tipo": tel.tipoTelefoneFornecedor.value
                        } for tel in telefones
                    ],
                    "preco_produto": preco
                })

            resultado.append({
                "id": produto.idProduto,
                "nome": produto.nomeProduto,
                "descricao": produto.descricaoProduto,
                "quantidade_estoque": produto.quantidadeEstoque,
                "fornecedores": fornecedores_lista
            })

        return resultado

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))