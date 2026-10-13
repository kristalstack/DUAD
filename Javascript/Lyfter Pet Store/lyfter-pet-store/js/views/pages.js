import { api, session, saveSession } from "../api.js";
import { link } from "../utils.js";
const app = document.querySelector("#app");
const user = () => session()?.user;
let notify, render;
export function configurePages(deps) { notify = deps.notify; render = deps.render; }

export function landing() {
  app.innerHTML = `<section class="hero"><div><p class="eyebrow">Todo para tus mejores amigos</p><h1>Su felicidad empieza aquí 🐾</h1><p>Descubre productos para consentir a tus mascotas. Compra de forma sencilla, segura y sin complicaciones.</p>${link(user() ? "Explorar productos" : "Comenzar a comprar", user() ? "#/catalog" : "#/register")}</div><div class="hero-art" aria-hidden="true">🐶🐱</div></section><h2>Una tienda pensada para ellos</h2><div class="grid"><article class="card">🚚 <strong>Compra fácil</strong><p>Elige, agrega al carrito y confirma tu pedido.</p></article><article class="card">💚 <strong>Cuidado con amor</strong><p>Productos para el bienestar de tus mascotas.</p></article><article class="card">🔒 <strong>Tu cuenta</strong><p>Consulta tus compras desde tu perfil.</p></article></div>`;
}
export function authPage(register) {
  app.innerHTML = `<section class="panel form"><h1>${register ? "Crear cuenta" : "Iniciar sesión"}</h1><form id="authForm" class="stack">${register ? '<label>Nombre completo<input name="name" minlength="2" maxlength="120" required autocomplete="name"></label>' : ""}<label>Correo electrónico<input name="email" type="email" required autocomplete="email"></label><label>Contraseña<input name="password" type="password" minlength="8" required autocomplete="${register ? "new-password" : "current-password"}"></label><button>${register ? "Registrarme" : "Ingresar"}</button></form><p>${register ? '¿Ya tienes cuenta? <a href="#/login">Ingresa aquí</a>' : '¿No tienes cuenta? <a href="#/register">Regístrate aquí</a>'}</p></section>`;
  document.querySelector("#authForm").onsubmit = async (e) => {
    e.preventDefault();
    const d = Object.fromEntries(new FormData(e.target));
    if (
      !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(d.email) ||
      d.password.length < 8 ||
      (register && d.name.trim().length < 2)
    ) {
      notify("Revisa los datos del formulario");
      return;
    }
    try {
      saveSession(await (register ? api.register(d) : api.login(d)));
      notify("Bienvenido a Lyfter Pet Store", true);
      location.hash = "#/catalog";
      render();
    } catch (err) {
      notify(err.message);
    }
  };
}

