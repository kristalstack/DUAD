import { api, session } from "../api.js";
import { esc, money } from "../utils.js";

const app = document.querySelector("#app");

let getCart;
let notify;
let render;
let clearStoredCart;

export function configureCheckout(dependencies) {
  getCart = dependencies.getCart;
  notify = dependencies.notify;
  render = dependencies.render;
  clearStoredCart = dependencies.clearStoredCart;
}

const user = () => session()?.user;

export async function checkoutPage() {
  const c = await getCart();
  if (!c?.items.length) {
    location.hash = "#/cart";
    return;
  }
  const { addresses } = await api.addresses(user().id);
  app.innerHTML = `<h1>Resumen del pedido</h1><div class="panel"><h2>Productos</h2>${c.items.map((i) => `<p>${esc(i.product.name)} × ${i.quantity} — ${money(Number(i.product.price) * i.quantity)}</p>`).join("")}<h2>Total: ${money(c.estimated_total)}</h2></div><section class="panel" class="panel panel-spaced"><h2>Dirección de facturación</h2><form id="checkoutForm" class="stack"><label>Selecciona una dirección<select name="address_id" ${addresses.length ? "required" : ""}>${addresses.map((a) => `<option value="${a.id}">${esc(a.recipient)} — ${esc(a.line1)}, ${esc(a.city)}</option>`).join("")}</select></label><label>Método de pago<select name="payment_method"><option value="TRANSFER">Transferencia (demostración)</option><option value="SINPE">SINPE (demostración)</option></select></label><label>Referencia del pago<input name="payment_reference" minlength="3" maxlength="100" required placeholder="Referencia de prueba"></label><p class="notice">Proyecto educativo: no se procesa ningún pago real. Confirmar registra la venta en el backend.</p><button ${addresses.length ? "" : "disabled"}>Confirmar compra</button></form>${addresses.length ? "" : "<p>Primero agrega una dirección.</p>"}<h3>Nueva dirección</h3><form id="addressForm" class="stack"><label>Destinatario<input name="recipient" required maxlength="120"></label><label>Calle y número<input name="line1" required maxlength="255"></label><label>Ciudad<input name="city" required maxlength="100"></label><label>Estado o provincia<input name="province" required maxlength="100"></label><label>País (código de dos letras)<input name="country" value="MX" pattern="[A-Za-z]{2}" required maxlength="2"></label><button class="secondary">Guardar dirección</button></form></section>`;
  document.querySelector("#addressForm").onsubmit = async (e) => {
    e.preventDefault();
    try {
      const d = Object.fromEntries(new FormData(e.target));
      d.country = d.country.toUpperCase();
      await api.addAddress(user().id, d);
      notify("Dirección guardada", true);
      checkoutPage();
    } catch (err) {
      notify(err.message);
    }
  };
  document.querySelector("#checkoutForm").onsubmit = async (e) => {
    e.preventDefault();
    const d = Object.fromEntries(new FormData(e.target));
    d.address_id = Number(d.address_id);
    try {
      const { invoice } = await api.checkout(c.id, d);
      clearStoredCart();
      sessionStorage.setItem("lyfter_last_invoice", JSON.stringify(invoice));
      location.hash = "#/success";
      render();
    } catch (err) {
      notify(err.message);
    }
  };
}