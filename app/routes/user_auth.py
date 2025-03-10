from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from app.database.config import get_db
from app.database.models import Login, Cliente
from app.utils.auth_utils import verificar_senha
from app.utils.security import criar_token_acesso, ACCESS_TOKEN_EXPIRE_MINUTES


router = APIRouter()

@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # Buscar usuário pelo CPF (username será o CPF)
    login = db.query(Login).filter(Login.cpfLogin == form_data.username).first()
    if not login:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    
    # Verificar senha
    if not verificar_senha(form_data.password, login.senhaLogin):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    
    # Buscar informações do cliente
    cliente = db.query(Cliente).filter(Cliente.idCliente == login.id_Cliente).first()
    
    # Criar token de acesso
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = criar_token_acesso(
        data={"user_id": login.id_Cliente, "nome": cliente.nomeCliente},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id_usuario": login.id_Cliente,
            "nome": cliente.nomeCliente
        }
    }
