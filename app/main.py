from fastapi import FastAPI
from app.routes import cadastro_produto, registro_cliente, user_auth, fornecedor, listar_produto, movimentar_produto, listar_movimentacoes



# Criar uma instância do FastAPI
app = FastAPI()


# Rota de Clientes
app.include_router(registro_cliente.router, tags=["Clientes"])
app.include_router(user_auth.router, tags=["Autenticação"])

# Rotas de Produtos
app.include_router(cadastro_produto.router, tags=["Produtos"])

# Rotas de Fornecedores
app.include_router(fornecedor.router, tags=["Fornecedores"])

# Rota de Listagem de Produtos
app.include_router(listar_produto.router, tags=["Listagem de Produtos"])

# Rotas de Movimentação de Produtos
app.include_router(movimentar_produto.router, tags=["Movimentação de Produtos"])

# Rotas de Listagem de Movimentações
app.include_router(listar_movimentacoes.router, tags=["Listagem de Movimentações"])