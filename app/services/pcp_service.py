from app.extensions import get_db

def resumo_dashboard():
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    linha,
                    SUM(hc_padrao) AS hc_planejado,
                    SUM(hc_real)   AS hc_real
                FROM lancamentos
                WHERE data = CURRENT_DATE
                GROUP BY linha
                ORDER BY linha
            """)
            rows = cur.fetchall()

    dados = []
    total_planejado = 0
    total_real = 0

    for r in rows:
        absenteismo = 0
        if r["hc_planejado"] > 0:
            absenteismo = round(
                (r["hc_planejado"] - r["hc_real"]) / r["hc_planejado"] * 100, 2
            )

        status = "OK" if r["hc_real"] >= r["hc_planejado"] else "CRÍTICO"

        item = {
            "nome": r["linha"],
            "hc_planejado": r["hc_planejado"],
            "hc_real": r["hc_real"],
            "absenteismo": absenteismo,
            "status": status
        }

        dados.append(item)

        total_planejado += r["hc_planejado"]
        total_real += r["hc_real"]

    # 🔴 TOP LINHAS COM MAIS ABSENTEÍSMO
    ranking_absenteismo = sorted(
        dados,
        key=lambda x: x["absenteismo"],
        reverse=True
    )

    abs_total = 0
    if total_planejado > 0:
        abs_total = round(
            (total_planejado - total_real) / total_planejado * 100, 2
        )

    return {
        "dados": dados,
        "ranking": ranking_absenteismo[:5],  # TOP 5 (padrão profissional)
        "kpis": {
            "hc_planejado": total_planejado,
            "hc_real": total_real,
            "absenteismo": abs_total,
            "linhas": len(dados)
        }
    }
