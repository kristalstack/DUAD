import { esc, money, link } from "../utils.js";
const app = document.querySelector("#app");

export function successPage() {
  let inv;
  try {
    inv = JSON.parse(sessionStorage.getItem("lyfter_last_invoice"));
  } catch {}
  app.innerHTML = `<div class="empty"><div class="hero-art">🎉</div><h1>¡Compra finalizada!</h1><p>Tu pedido fue registrado correctamente.</p>${inv ? `<p>Factura: <strong>${esc(inv.number)}</strong></p><h2>${money(inv.total)}</h2>` : ""}${link("Seguir comprando", "#/catalog")}</div>`;
}