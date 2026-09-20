/* Abre el modal de confirmación al pulsar "Elegir" en una tarjeta o en un popup del mapa (FN-4 / FN-20). */
document.addEventListener("click", (e) => {
  const btn = e.target.closest("[data-elegir]");
  if (!btn) return;
  document.getElementById("elegirNombre").textContent = btn.dataset.nombre;
  bootstrap.Modal.getOrCreateInstance(document.getElementById("modalElegir")).show();
});
