import { api, session, saveSession } from "./api.js";
import {
  catalog,
  productPage,
  configureCatalog,
} from "./views/catalog.js";
import { cartPage, configureCart } from "./views/cart.js";
import { checkoutPage, configureCheckout } from "./views/checkout.js";
import { successPage } from "./views/success.js";
import { adminPage, editPage, configureAdmin } from "./views/admin.js";
import { landing, authPage, configurePages } from "./views/pages.js";
import { esc } from "./utils.js";
import { readStoredCart, storeCart, clearStoredCart } from "./cart-storage.js";
const app = document.querySelector("#app"),
  nav = document.querySelector("#nav"),
  toast = document.querySelector("#toast");
const user = () => session()?.user;
const isAdmin = () => user()?.role === "admin";
let toastTimer;
function notify(msg, ok = false) {
  clearTimeout(toastTimer);
  toast.textContent = msg;
  toast.className = ok ? "ok" : "";
  toast.style.display = "block";
  toastTimer = setTimeout(() => { toast.style.display = "none"; }, 4500);
}
function navRender() {
  nav.innerHTML = user()
    ? `<a href="#/catalog">Catálogo</a><a href="#/cart">Carrito</a>${isAdmin() ? '<a href="#/admin">Administración</a>' : ""}<span class="muted">Hola, ${esc(user().name)}</span><button id="logout" class="secondary">Salir</button>`
    : '<a href="#/">Inicio</a><a href="#/login">Ingresar</a><a class="btn" href="#/register">Crear cuenta</a>';
  document.querySelector("#logout")?.addEventListener("click", async () => {
    try {
      await api.logout();
    } catch {}
    clearStoredCart(user()?.id);
    saveSession(null);
    location.hash = "#/";
    render();
  });
}
async function getCart(create = false) {
  const { carts } = await api.carts();
  const saved = readStoredCart(user()?.id);
  // Prefer the persisted cart if it is still open and belongs to this account.
  let c = carts.find((x) => x.status === "open" && x.id === saved?.id)
    ?? carts.find((x) => x.status === "open");
  if (!c && create) c = (await api.newCart()).cart;
  storeCart(user()?.id, c);
  return c;
}
async function addToCart(id) {
  const { product } = await api.product(id);
  const c = await getCart(true);
  const qty = (c.items.find((x) => x.product_id === id)?.quantity || 0) + 1;
  if (qty > product.stock) throw Error("No hay suficiente stock");
  await api.setItem(c.id, id, qty);
  await getCart();
}
configureCatalog({
  addToCart,
  notify,
});
configureCheckout({
  getCart,
  notify,
  render,
  clearStoredCart: () => clearStoredCart(user()?.id),
});

configureCart({
  getCart,
  notify,
  refreshCart: () => getCart(),
});
configureAdmin({ notify, render });
configurePages({ notify, render });

async function render() {
  navRender();
  const [page, id] = location.hash.replace(/^#\/?/, "").split("/");
  if (!user() && !["", "login", "register"].includes(page)) {
    location.hash = "#/login";
    return;
  }
  if (["admin", "edit"].includes(page) && !isAdmin()) {
    app.innerHTML =
      '<div class="empty">Acceso restringido a administradores.</div>';
    return;
  }
  try {
    switch (page) {
      case "":
        landing();
        break;
      case "login":
        authPage(false);
        break;
      case "register":
        authPage(true);
        break;
      case "catalog":
        await catalog();
        break;
      case "product":
        await productPage(id);
        break;
      case "cart":
        await cartPage();
        break;
      case "checkout":
        await checkoutPage();
        break;
      case "success":
        successPage();
        break;
      case "admin":
        await adminPage();
        break;
      case "edit":
        await editPage(id);
        break;
      default:
        app.innerHTML = "<h1>Página no encontrada</h1>";
    }
  } catch (e) {
    app.innerHTML = `<div class="empty"><h2>No se pudo cargar esta página</h2><p>${esc(e.message)}</p><button id="retry">Reintentar</button></div>`;
    document.querySelector("#retry").onclick = render;
    notify(e.message);
  }
}
window.addEventListener("lyfter:session-expired", () => {
  location.hash = "#/login";
  render();
  notify("Tu sesión expiró. Inicia sesión nuevamente.");
});
window.addEventListener("hashchange", render);
render();
