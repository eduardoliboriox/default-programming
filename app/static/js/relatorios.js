document.getElementById("formRelatorio").addEventListener("submit", async function (e) {
  e.preventDefault();

  const formData = new FormData(this);
  const params = new URLSearchParams(formData);

  const resultado = document.getElementById("resultadoRelatorio");
  resultado.innerHTML = `
    <div class="alert alert-info">
      <i class="bi bi-hourglass-split"></i> Gerando relatório...
    </div>
  `;

  try {
    const response = await fetch(`/api/relatorios?${params.toString()}`);
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Erro ao gerar relatório");
    }

    resultado.innerHTML = `
      <div class="card shadow-sm">
        <div class="card-header bg-light">
          <strong>Período:</strong> ${data.periodo}
        </div>

        <div class="card-body">
          <h5 class="mb-3">
            <i class="bi bi-bar-chart"></i>
            Ranking de Linhas por Faltas
          </h5>

          <ul class="list-group mb-4">
            ${data.linhas.map(l => `
              <li class="list-group-item">
                <div class="d-flex justify-content-between align-items-center">
                  <strong>${l.linha}</strong>
                  <span class="badge bg-danger fs-6">${l.total_faltas}</span>
                </div>

                ${l.cargo_critico ? `
                  <div class="mt-1">
                    <small class="text-muted">
                      Cargo crítico:
                      <strong>${l.cargo_critico.cargo}</strong>
                      — ${l.cargo_critico.percentual_linha}% da linha
                    </small>
                  </div>
                ` : ""}
              </li>
            `).join("")}
          </ul>

          ${data.cargo_critico ? `
            <div class="alert alert-warning">
              <strong>Cargo mais impactante no período:</strong>
              ${data.cargo_critico.nome}
              (${data.cargo_critico.total} faltas)
            </div>
          ` : ""}
        </div>
      </div>
    `;
  } catch (error) {
    resultado.innerHTML = `
      <div class="alert alert-danger">
        <i class="bi bi-exclamation-triangle"></i>
        ${error.message}
      </div>
    `;
  }
});
