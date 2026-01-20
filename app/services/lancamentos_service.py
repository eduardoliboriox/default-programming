from app.repositories import lancamentos_repository

def calcular_absenteismo(hc_padrao, hc_real):
    if hc_padrao <= 0:
        return 0
    return round((hc_padrao - hc_real) / hc_padrao * 100, 2)

def criar_lancamento(dados):
    # transforma ImmutableMultiDict em dict normal
    dados = dict(dados)

    absenteismo = calcular_absenteismo(
        int(dados["hc_padrao"]),
        int(dados["hc_real"])
    )

    dados["absenteismo"] = absenteismo

    lancamentos_repository.inserir(dados)

    return {
        "sucesso": True,
        "absenteismo": absenteismo
    }

