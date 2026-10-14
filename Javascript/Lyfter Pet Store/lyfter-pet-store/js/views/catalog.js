import { api } from "../api.js";
import { esc, money } from "../utils.js";

const app = document.querySelector("#app");

let addToCart;
let notify;

export function configureCatalog(dependencies) {
  addToCart = dependencies.addToCart;
  notify = dependencies.notify;
}

function productCard(p) {
  return `<article class="card"><div class="product-art" aria-hidden="true">🐾</div><span class="muted">${esc(p.sku)}</span><h3>${esc(p.name)}</h3><p class="muted">${esc(p.description || "Un favorito para tu mascota.")}</p><div class="row"><span class="price">${money(p.price)}</span><span class="pill">${p.stock} disponibles</span></div><div class="row"><a href="#/product/${p.id}">Ver detalles →</a><button data-add="${p.id}" ${p.stock < 1 ? "disabled" : ""}>Agregar</button></div></article>`;
}

export async function catalog() { 
  app.innerHTML = "<h1>Catálogo de productos</h1><p>Cargando productos…</p>";
  const { products } = await api.products();
  const active = products.filter((p) => p.active);
  app.innerHTML = `<div class="row"><div><p class="eyebrow">Nuestra selección</p><h1>Catálogo de productos</h1></div><span>${active.length} productos</span></div>${active.length ? `<div class="grid">${active.map(productCard).join("")}</div>` : '<div class="empty"><h2>El catálogo está vacío</h2><p>Pronto tendremos nuevos productos.</p></div>'}`;
  bindAdd();
}
function bindAdd() {
  document.querySelectorAll("[data-add]").forEach(
    (b) =>
      (b.onclick = async () => {
        try {
          await addToCart(Number(b.dataset.add));
          notify("Producto agregado al carrito", true);
        } catch (e) {
          notify(e.message);
        }
      }),
  );
}
export async function productPage(id) {
  const { product: p } = await api.product(id);
  app.innerHTML = `<a href="#/catalog">← Volver al catálogo</a><section class="panel" class="panel panel-spaced"><div class="product-art">🐾</div><p class="eyebrow">${esc(p.sku)}</p><h1>${esc(p.name)}</h1><p>${esc(p.description || "Producto para mascotas")}</p><p class="price">${money(p.price)}</p><p>${p.stock} unidades disponibles</p><button data-add="${p.id}" ${p.stock < 1 ? "disabled" : ""}>Agregar al carrito</button></section>`;
  bindAdd();
}