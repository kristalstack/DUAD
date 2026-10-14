import { api } from "../api.js";
import { esc, money, link } from "../utils.js";

const app = document.querySelector("#app");

let getCart;
let notify;
let refreshCart;

export function configureCart(dependencies) {
  getCart = dependencies.getCart;
  notify = dependencies.notify;
  refreshCart = dependencies.refreshCart;
}

export async function cartPage() {
  const c = await getCart();
  if (!c || !c.items.length) {
    app.innerHTML = `<div class="empty"><h1>Tu carrito está vacío 🛒</h1>${link("Explorar catálogo", "#/catalog")}</div>`;
    return;
  }
  app.innerHTML = `<h1>Tu carrito</h1><div class="panel stack">${c.items.map((i) => `<div class="row"><div><strong>${esc(i.product.name)}</strong><p>${money(i.product.price)} c/u</p></div><div class="row"><label>Cantidad <input class="qty" data-qty="${i.product_id}" type="number" min="1" max="${i.product.stock}" value="${i.quantity}"></label><button class="danger" data-remove="${i.product_id}">Eliminar</button></div></div>`).join("")}<div class="row"><h2>Total: ${money(c.estimated_total)}</h2>${link("Revisar pedido", "#/checkout")}</div></div>`;
  document.querySelectorAll("[data-qty]").forEach(
    (el) =>
      (el.onchange = async () => {
        try {
          const q = Number(el.value);
          if (!Number.isInteger(q) || q < 1 || q > Number(el.max))
            throw Error("Cantidad inválida o superior al stock");
          await api.setItem(c.id, Number(el.dataset.qty), q);
          await refreshCart();
          cartPage();
        } catch (e) {
          notify(e.message);
          cartPage();
        }
      }),
  );
  document.querySelectorAll("[data-remove]").forEach(
    (el) =>
      (el.onclick = async () => {
        try {
          await api.removeItem(c.id, Number(el.dataset.remove));
          await refreshCart();
          cartPage();
        } catch (e) {
          notify(e.message);
        }
      }),
  );
}