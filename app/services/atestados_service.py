from app.repositories import atestados_repository
from app.config import Config

SENHAS = {
    "ATESTADO": Config.SENHA_ATESTADO,
    "ABONO": Config.SENHA_ABONO
}

def registrar_atestado(dados):
    tipo = dados["tipo"]
    senha = dados["senha"]

    if SENHAS.get(tipo) != senha:
        return {"success": False, "error": "Senha inválida"}

    atestados_repository.inserir(
        data=dados["data"],
        matricula=dados["matricula"],
        cargo_id=dados["cargo_id"],
        tipo=tipo
    )

    return {"success": True}
