from app.repositories import modelos_repository
from app.repositories.modelos_repository import buscar_ultimo_modelo
import math
def calcular_absenteismo(hc_planejado, hc_real):
    if hc_planejado == 0:
        return 0
    return round((hc_planejado - hc_real) / hc_planejado * 100, 2)


def status_linha(hc_planejado, hc_real):
    return "OK" if hc_real >= hc_planejado else "CRÍTICO"
