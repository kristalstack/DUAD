import { api } from "../api.js";
import { esc, money, link } from "../utils.js";
const app = document.querySelector("#app");
let notify, render;
export function configureAdmin(deps) { notify = deps.notify; render = deps.render; }

export async function adminPage() {
  const [{ products }, { invoices }] = await Promise.all([
    api.products(),
    api.invoices(),
  ]);
  app.innerHTML = `<h1>Panel de administración</h1><div class="grid"><div class="card"><span>Productos</span><h2>${products.length}</h2></div><div class="card"><span>Unidades en inventario</span><h2>${products.reduce((a, p) => a + p.stock, 0)}</h2></div><div class="card"><span>Facturas</span><h2>${invoices.length}</h2></div></div><h2>Inventario</h2><div class="table-wrap"><table><thead><tr><th>Producto</th><th>SKU</th><th>Precio</th><th>Stock</th><th>Estado</th><th>Acción</th></tr></thead><tbody>${products.map((p) => `<tr><td>${esc(p.name)}</td><td>${esc(p.sku)}</td><td>${money(p.price)}</td><td>${p.stock}</td><td>${p.active ? "Activo" : "Inactivo"}</td><td><a href="#/edit/${p.id}">Editar</a></td></tr>`).join("")}</tbody></table></div><p>${link("Crear producto", "#/edit/new")}</p><h2>Ventas</h2><div class="table-wrap"><table><thead><tr><th>Factura</th><th>Cliente</th><th>Correo electrónico</th><th>Estado</th><th>Total</th></tr></thead><tbody>${invoices.map((i) => `<tr><td>${esc(i.number)}</td><td>${esc(i.customer?.name || `ID ${i.user_id}`)}</td><td>${esc(i.customer?.email || "—")}</td><td>${esc(i.status)}</td><td>${money(i.total)}</td></tr>`).join("")}</tbody></table></div>`;
}
export async function editPage(id) {
  const fresh = id === "new",
    p = fresh
      ? {
          name: "",
          sku: "",
          description: "",
          price: "",
          stock: 0,
          active: true,
        }
      : (await api.product(id)).product;
  app.innerHTML = `<section class="panel form"><a href="#/admin">← Administración</a><h1>${fresh ? "Nuevo producto" : "Editar producto"}</h1><form id="productForm" class="stack"><label>Nombre<input name="name" value="${esc(p.name)}" required maxlength="160"></label><label>SKU<input name="sku" value="${esc(p.sku)}" required maxlength="60"></label><label>Descripción<textarea name="description">${esc(p.description || "")}</textarea></label><label>Precio<input name="price" type="number" step="0.01" min="0" value="${esc(p.price)}" required></label><label>Stock<input name="stock" type="number" step="1" min="0" value="${p.stock}" required></label><label><input type="checkbox" name="active" ${p.active ? "checked" : ""} > Producto activo</label><button>Guardar producto</button></form></section>`;
  document.querySelector("#productForm").onsubmit = async (e) => {
    e.preventDefault();
    const form = e.target,
      d = Object.fromEntries(new FormData(form));
    d.price = Number(d.price);
    d.stock = Number(d.stock);
    d.active = form.elements.active.checked;
    if (
      !Number.isFinite(d.price) ||
      d.price < 0 ||
      !Number.isInteger(d.stock) ||
      d.stock < 0 ||
      !d.name.trim() ||
      !d.sku.trim()
    ) {
      notify("Revisa los datos del producto");
      return;
    }
    try {
      await (fresh ? api.createProduct(d) : api.updateProduct(id, d));
      notify("Producto guardado", true);
      location.hash = "#/admin";
      render();
    } catch (err) {
      notify(err.message);
    }
  };
}
