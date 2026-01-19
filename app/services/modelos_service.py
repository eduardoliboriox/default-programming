from app.repositories import modelos_repository

def listar_codigos():
    return modelos_repository.listar_codigos()

def listar_modelos():
    return modelos_repository.listar_modelos()

def cadastrar_modelo(dados):
    modelos_repository.inserir(dados)
    return {"sucesso": True}

def excluir_modelo(dados):
    modelos_repository.excluir(dados["codigo"], dados["fase"])
    return {"sucesso": True}

def calcular_absenteismo(hc_planejado, hc_real):
    if hc_planejado == 0:
        return 0
    return round((hc_planejado - hc_real) / hc_planejado * 100, 2)

def status_linha(hc_planejado, hc_real):
    return "OK" if hc_real >= hc_planejado else "CRÍTICO"

def resumo_dashboard():
    linhas = [
        {"nome": "Linha 1", "hc_planejado": 10, "hc_real": 9},
        {"nome": "Linha 2", "hc_planejado": 8, "hc_real": 8},
    ]

    for l in linhas:
        l["absenteismo"] = calcular_absenteismo(
            l["hc_planejado"], l["hc_real"]
        )

    return {"dados": linhas}
