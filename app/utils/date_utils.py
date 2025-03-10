from datetime import datetime
from fastapi import HTTPException




def converter_data_para_datetime(data_str: str) -> datetime:
    """
    Converte uma string de data no formato DD/MM/YYYY para um objeto datetime.
    Args:
        data_str (str): A string da data no formato DD/MM/YYYY
    Returns:
        datetime: O objeto datetime correspondente à data fornecida
    Raises:
        HTTPException: Se o formato da data fornecida não for válido
    """

    try:
        return datetime.strptime(data_str, "%d/%m/%Y")
    except ValueError:
        raise HTTPException(status_code=400,
                            detail="Formato de data inválido. Use o formato YYYY-MM-DD"
                            )
    

def verificar_idade_maior_que_15(data_nascimento: datetime) -> bool:
    """
    Verifica se a data de nascimento do usuário é maior que 15 anos.
    Args:
        data_nascimento (datetime): A data de nascimento do usuário
    Returns:
        bool: True se a idade do usuário é maior que 15 anos, False caso contrário
    """
    idade = datetime.now().year - data_nascimento.year
    return idade >= 15
