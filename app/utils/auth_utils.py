from passlib.context import CryptContext

# Criar o contexto para hashing de senha usando bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verificar_senha(senha_texto: str, senha_hash: str) -> bool:
    """
    Verifica se a senha em texto corresponde ao hash armazenado
    """
    return pwd_context.verify(senha_texto, senha_hash)

def gerar_hash_senha(senha: str) -> str:
    """
    Gera um hash da senha fornecida
    """
    return pwd_context.hash(senha)