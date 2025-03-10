from models import *
from config import engine





# Criar as tabelas no banco de dados

def create_databases():
    Produto.__table__.create(bind=engine)

    Movimentacao.__table__.create(bind=engine)

    Fornecedor.__table__.create(bind=engine)

    TelefoneFornecedor.__table__.create(bind=engine)

    FornecedorProduto.__table__.create(bind=engine)

    Cliente.__table__.create(bind=engine)

    Login.__table__.create(bind=engine)

