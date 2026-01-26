async function atualizarPowerBI() {
  try {
    const params = new URLSearchParams({
      data_inicial: document.querySelector('[name="data_inicial"]').value,
      data_final: document.querySelector('[name="data_final"]').value,
      turno: document.querySelector('[name="turno"]').value,
      filial: document.querySelector('[name="filial"]').value,
      setor: document.querySelector('[name="setor"]').value,
      linha: document.querySelector('[name="linha"]').value
    });

    const resp = await fetch(`/api/powerbi/resumo?${params}`);
    const data = await resp.json();

    // ===== KPIs =====
    document.querySelector("#kpi-hc-planejado").innerText = data.kpis.hc_planejado;
    document.querySelector("#kpi-hc-real").innerText = data.kpis.hc_real;
    document.querySelector("#kpi-ausencias").innerText = data.kpis.ausencias;
    document.querySelector("#kpi-abs").innerText = data.kpis.absenteismo + "%";
    document.querySelector("#kpi-linhas").innerText = data.kpis.linhas;

    // ===== RANKING DE LINHAS =====
    const container = document.querySelector("#rankingPowerBI");
    container.innerHTML = "";

    const max = Math.max(...data.ranking_faltas.map(l => l.altura), 1);

    data.ranking_faltas.forEach(l => {
      container.innerHTML += `
        <div class="text-center" style="width:60px; cursor:pointer"
             onclick="abrirModalLinhaPowerBI('${l.linha}')">
          <div class="fw-bold small">${l.faltas}</div>
          <div style="
            height:${(l.altura * 180) / max}px;
            background:${l.status === 'CRITICO' ? '#dc3545' : '#198754'};
            border-radius:6px;">
          </div>
          <small>${l.linha}</small>
        </div>
      `;
    });

  } catch (e) {
    console.error("Erro ao atualizar PowerBI", e);
  }
}

// Polling inteligente
setInterval(atualizarPowerBI, 5000);
document.addEventListener("DOMContentLoaded", atualizarPowerBI);
