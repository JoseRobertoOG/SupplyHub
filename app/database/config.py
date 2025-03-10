from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Endereço do banco de dados
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/supplyhub_db" # Endereço do banco de dados

# Criação do motor do banco de dados
engine = create_engine(SQLALCHEMY_DATABASE_URL) # Criar o motor do banco de dados

# Criação da sessão local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # Criar a sessão local

# Criação do modelo base
Base = declarative_base()

# Função para obter uma sessão do banco de dados
def get_db(): # Criar e fechar coneccoes corretamente
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
