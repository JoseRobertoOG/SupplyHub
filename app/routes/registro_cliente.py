from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.utils.date_utils import converter_data_para_datetime, verificar_idade_maior_que_15
from app.utils.auth_utils import gerar_hash_senha
from app.database.models import Cliente, Login
from app.database.config import get_db
import re



router = APIRouter()


@router.post("/signup/")

def registrar_cliente(nome_cliente: str,
                      cpf_cliente: str,
                      email_cliente: str,
                      data_nascimento_cliente: str,
                      senha_cliente: str,
                      senha_confirmacao: str,
                      db: Session = Depends(get_db)
                      ):
    
    try:
        # Verificar se o nome do cliente é válido
        if not re.match(r"^[a-zA-Z\s]+$", nome_cliente):
            raise HTTPException(status_code=400, detail="Nome inválido")
        

        # Verificar se o CPF já está cadastrado
        cpf_existente = db.query(Cliente).filter(Cliente.cpfCliente == cpf_cliente).first()
        if cpf_existente:
            raise HTTPException(status_code=400, detail="CPF já cadastrado")

        # Verificar se o CPF é válido
        if not re.match(r"^\d{11}$", cpf_cliente):
            raise HTTPException(status_code=400, detail="CPF inválido")
        

        # Verificar se o email já está cadastrado
        email_existente = db.query(Cliente).filter(Cliente.emailCliente == email_cliente).first()      
        if email_existente: 
            raise HTTPException(status_code=400, detail="Email já cadastrado")
        
        # Verificar se o email é válido
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email_cliente):
            raise HTTPException(status_code=400, detail="Email inválido")
        

        # Verificar se a data de nascimento é válida
        data_nascimento = converter_data_para_datetime(data_nascimento_cliente) # A funcao ja retona erro se a data nao estiver no formato dd/mm/yyyy

        idade = verificar_idade_maior_que_15(data_nascimento)
        if not idade:
            raise HTTPException(status_code=400, detail="O cliente deve ter pelo menos 15 anos")


        # Verificar se as senhas coincidem
        if senha_cliente != senha_confirmacao:
            raise HTTPException(status_code=400, detail="As senhas não coincidem")
        
        # Verifica se a senha tem pelo menos 8 caracteres
        if len(senha_cliente) < 8:
            raise HTTPException(status_code=400, detail="A senha deve ter pelo menos 8 caracteres")
        
        # Verificar se a senha contem pelo menos um numero
        if not re.search(r"\d", senha_cliente):
            raise HTTPException(status_code=400, detail="A senha deve conter pelo menos um número")
        



        # Criar novo cliente
        db_cliente = Cliente(nomeCliente = nome_cliente,
                             cpfCliente = cpf_cliente,
                             emailCliente = email_cliente,
                             dataNascimentoCliente = data_nascimento
                             )
        
        # Adicionar cliente ao banco de dados
        db.add(db_cliente)
        db.commit()
        db.refresh(db_cliente)


        # Adicionar login ao banco de dados
        senha_hasheada = gerar_hash_senha(senha_cliente)
        db_login = Login(cpfLogin = cpf_cliente,
                         senhaLogin = senha_hasheada,
                         id_Cliente = db_cliente.idCliente
                         )
        
        db.add(db_login)
        db.commit()
        db.refresh(db_login)

        return db_cliente
    

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))