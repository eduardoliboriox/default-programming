document.getElementById("setorSelect").addEventListener("change", async e => {
  const setor = e.target.value;
  const linhaSelect = document.getElementById("linhaSelect");

  linhaSelect.innerHTML = "<option>Todas</option>";

  if (setor === "Todos") return;

  const resp = await fetch(`/api/linhas?setor=${setor}`);
  const linhas = await resp.json();

  linhas.forEach(l => {
    const opt = document.createElement("option");
    opt.textContent = l;
    linhaSelect.appendChild(opt);
  });
});

// Toggle "Ver mais" linhas no Power BI
function toggleLinhasPowerBI() {
  const extras = document.querySelectorAll(".extra-linha-powerbi");
  if (!extras.length) return;

  const btn = document.getElementById("toggleLinhasPowerBIBtn");
  const isHidden = extras[0].classList.contains("d-none");

  extras.forEach(el => el.classList.toggle("d-none", !isHidden));
  btn.textContent = isHidden ? "Recolher" : "Ver mais";
}

