from fastapi import APIRouter, HTTPException, Depends
from app.database.models import Fornecedor, TelefoneFornecedor, FornecedorProduto, TipoTelefoneFornecedor, Produto
from sqlalchemy.orm import Session
from app.database.config import get_db
from app.utils.security import get_current_user
import re


router = APIRouter()


@router.post("/fornecedor/{produto_id}",
    summary="Cadastrar novo fornecedor",
    description="Cadastra um novo fornecedor com seus telefones e vincula a um produto existente"
)
async def cadastro_fornecedor(
    produto_id: int,
    nome: str,
    email: str,
    preco_produto: float,
    telefone1: str,
    tipo_telefone1: TipoTelefoneFornecedor,
    telefone2: str | None = None,
    tipo_telefone2: TipoTelefoneFornecedor | None = None,
    telefone3: str | None = None,
    tipo_telefone3: TipoTelefoneFornecedor | None = None,
    current_user: int = Depends(get_current_user),

    db: Session = Depends(get_db)
):
    try:
        # Verificar se o produto pertence ao cliente atual
        produto = db.query(Produto).filter(
            Produto.idProduto == produto_id,
            Produto.id_Cliente == current_user
            ).first()
        
        if not produto:
            raise HTTPException(
                status_code=404,
                detail="Produto não encontrado ou não autorizado"
            )
        
        # Criar lista de telefones não nulos
        telefones = []
        if telefone1:
            telefones.append({"numero": telefone1, "tipo": tipo_telefone1})
        if telefone2:
            telefones.append({"numero": telefone2, "tipo": tipo_telefone2})
        if telefone3:
            telefones.append({"numero": telefone3, "tipo": tipo_telefone3})


        # Verifica se os telefones são validos
        for tel in telefones:
            if not re.match(r"^\d{11}$", tel["numero"]):
                raise HTTPException(status_code=400, detail="Telefone inválido")
            
            # Verifica se o tipo de telefone é valido
            if not isinstance(tel["tipo"], TipoTelefoneFornecedor):
                raise HTTPException(status_code=400, detail="Tipo de telefone inválido")
                    
        
        # Verifica se o email é valido
        if not re.match(r"^[^@]+@[^@]+\.[^@]+$", email):
            raise HTTPException(status_code=400, detail="Email inválido")
        

        # Verifica se o preco do produto é positivo
        if preco_produto <= 0:
            raise HTTPException(status_code=400, detail="O preço do produto deve ser positivo")
        
        
        
        # Criar o fornecedor
        db_fornecedor = Fornecedor(
            nomeFornecedor=nome,
            emailFornecedor=email
        )
        db.add(db_fornecedor)
        db.commit()
        db.refresh(db_fornecedor)
        
        # Adicionar os telefones
        for tel in telefones:
            db_telefone = TelefoneFornecedor(
                numeroTelefoneFornecedor=tel["numero"],
                tipoTelefoneFornecedor=tel["tipo"],
                id_Fornecedor=db_fornecedor.idFornecedor
            )
            db.add(db_telefone)
        
        # Criar relação com o produto
        fornecedor_produto = FornecedorProduto(
            precoFornecedorProduto=preco_produto,
            id_Fornecedor=db_fornecedor.idFornecedor,
            id_Produto=produto_id
        )
        db.add(fornecedor_produto)
        
        db.commit()
        
        return {
            "message": "Fornecedor cadastrado com sucesso",
            "fornecedor_id": db_fornecedor.idFornecedor
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))