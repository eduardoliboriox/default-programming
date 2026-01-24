async function salvarAtestado() {
  const payload = {
    data: document.querySelector("[name='data']").value,
    matricula: document.querySelector("[name='matricula_atestado']").value,
    cargo_id: document.querySelector("[name='cargo_atestado']").value,
    tipo: document.querySelector("[name='tipo_atestado']").value,
    senha: document.querySelector("[name='senha_atestado']").value
  };

  const resp = await fetch("/api/atestados", {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify(payload)
  });

  const res = await resp.json();

  alert(res.success ? "Registro efetuado" : res.error);
}
