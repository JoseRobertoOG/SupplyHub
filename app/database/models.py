from sqlalchemy import Column, Integer, DateTime, Float, ForeignKey, VARCHAR, CHAR, Enum
from app.database.config import Base
from datetime import datetime
import enum




# Enum para os tipos de movimentações
class TipoMovimentacao(enum.Enum):
    ENTRADA = 'entrada'
    SAIDA = 'saida'

# Enum para o modelo de telefone de fornecedor
class TipoTelefoneFornecedor(enum.Enum):
    VENDEDOR = 'vendedor'
    COMERCIAL = 'comercial'



# Modelo de cliente
class Cliente(Base):
    __tablename__ = 'cliente'

    idCliente = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    nomeCliente = Column(VARCHAR(100), nullable=False)
    cpfCliente = Column(CHAR(11), nullable=False, unique=True)
    emailCliente = Column(VARCHAR(100), nullable=False, unique=True)
    dataNascimentoCliente = Column(DateTime, nullable=False)



# Modelo de login
class Login(Base):
    __tablename__ = "login"

    idLogin = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    cpfLogin = Column(CHAR(11), nullable=False, unique=True)
    senhaLogin = Column(VARCHAR(255), nullable=False)
    id_Cliente = Column(Integer,
                        ForeignKey("cliente.idCliente",
                                   onupdate="CASCADE", # Atualiza caso o id do cliente seja alterado
                                   ondelete="CASCADE", # Deleta caso o cliente seja deletado    
                                   deferrable=True, # Adia a constraint até o commit
                                   initially="DEFERRED", # A verificação é feita após o commit
                                   name="FK_cliente_login"
                                   ),
                        unique=True,
                        nullable=False)
    


# Modelo de produto
class Produto(Base):
    __tablename__ = "produto"

    idProduto = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    nomeProduto = Column(VARCHAR(100), nullable=False)
    descricaoProduto = Column(VARCHAR(255), nullable=True)
    quantidadeEstoque = Column(Integer, nullable=False)
    dataCriacao = Column(DateTime, default=datetime.now)
    id_Cliente = Column(Integer,
                        ForeignKey("cliente.idCliente",
                                    ondelete="CASCADE", # Deleta caso o cliente seja deletado
                                    onupdate="CASCADE", # Atualiza caso o id do cliente seja alterado
                                    name="FK_cliente_produto"
                                    ),
                        nullable=False)
      


# Modelo de movimentação
class Movimentacao(Base):
    __tablename__ = "movimentacao"

    idMovimentacao = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    quantidadeMovimentada = Column(Integer, nullable=False)
    tipoMovimentacao = Column(Enum(TipoMovimentacao), nullable=False)
    dataMovimentacao = Column(DateTime, default=datetime.now)
    id_Produto = Column(Integer,
                        ForeignKey("produto.idProduto",
                                   onupdate="CASCADE", # Atualiza caso o id do produto seja alterado
                                   name="FK_produto_movimentacao"
                                   ),
                        nullable=False)
    id_Cliente = Column(Integer,
                        ForeignKey("cliente.idCliente",
                                   onupdate="CASCADE", # Atualiza caso o id do cliente seja alterado
                                   name="FK_cliente_movimentacao"
                                   ),
                        nullable=False)



# Modelo de fornecedor
class Fornecedor(Base):
    __tablename__ = "fornecedor"

    idFornecedor = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    nomeFornecedor = Column(VARCHAR(100), nullable=False)
    emailFornecedor = Column(VARCHAR(100), nullable=False, unique=True)



# Modelo de telefone de fornecedor
class TelefoneFornecedor(Base):
    __tablename__ = "telefoneFornecedor"

    idTelefoneFornecedor = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    numeroTelefoneFornecedor = Column(VARCHAR(11), nullable=False, unique=True)
    tipoTelefoneFornecedor = Column(Enum(TipoTelefoneFornecedor), nullable=False)
    id_Fornecedor = Column(Integer,
                           ForeignKey("fornecedor.idFornecedor",
                                      onupdate="CASCADE", # Atualiza caso o id do fornecedor seja alterado
                                      ondelete="CASCADE", # Deleta caso o fornecedor seja deletado
                                      deferrable=True, # Adia a constraint até o commit, necessário pois o o fornecedor e o cliente são criados simultaneamente
                                      initially="DEFERRED", # A verificação é feita após o commit
                                      name="FK_fornecedor_telefone"
                                      ),
                           nullable=False)



# Modelo de produto de fornecedor
class FornecedorProduto(Base):
    __tablename__ = "fornecedorProduto"

    idFornecedorProduto = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    precoFornecedorProduto = Column(Float, nullable=False)
    id_Fornecedor = Column(Integer,
                           ForeignKey("fornecedor.idFornecedor",
                                      onupdate="CASCADE", # Atualiza caso o id do fornecedor seja alterado
                                      ondelete="CASCADE", # Deleta caso o fornecedor seja deletado
                                      name="FK_fornecedor_fornecedorProduto"
                                      ),
                           nullable=False)
    id_Produto = Column(Integer,
                        ForeignKey("produto.idProduto",
                                   onupdate="CASCADE", # Atualiza caso o id do produto seja alterado
                                   ondelete="CASCADE", # Deleta caso o produto seja deletado
                                   name="FK_produto_fornecedorProduto"
                                   ),
                        nullable=False)