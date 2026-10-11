# Lyfter Pet Store — Frontend final 🐾

Interfaz de e-commerce para la API Flask **PetShop API** del módulo anterior. Desarrollada con HTML5 semántico, CSS3 (Grid y Flexbox, unidades relativas) y JavaScript ES Modules, sin frameworks.

## Requisitos

- Python 3 (para servir el frontend y hacer proxy de API; no necesita dependencias extra).
- Backend Flask PetShop funcionando en `http://127.0.0.1:5000` con PostgreSQL configurado. Consulta el README del backend para instalar dependencias, crear base de datos y administrador. Redis es opcional en la configuración del backend si no se define `REDIS_HOST`.

## Ejecución

1. Inicia Flask desde la carpeta del backend, con su entorno virtual y configuración `.env` preparados:
   ```bash
   flask --app run.py run --debug
   ```
2. En otra terminal, entra en la carpeta `lyfter-pet-store` y ejecuta:
   ```bash
   python3 serve.py
   ```
3. Abre **http://127.0.0.1:8000** (no abras el HTML mediante `file://`).
4. Registra un usuario para probar la tienda. Para probar el panel de administración, crea un admin mediante `flask --app run.py create-admin` desde el backend e inicia sesión con esa cuenta.
5. Desde el administrador crea productos. El catálogo muestra los productos activos del backend.

## Páginas y rutas

- `#/` — Landing page
- `#/register`, `#/login` — Registro e inicio de sesión
- `#/catalog`, `#/product/:id` — Catálogo y detalle
- `#/cart`, `#/checkout`, `#/success` — Carrito, resumen y confirmación
- `#/admin`, `#/edit/:id`, `#/edit/new` — Inventario, ventas y mantenimiento de productos (solo admin)

## Arquitectura y decisiones técnicas

- `index.html`: estructura HTML y puntos de montaje.
- `styles.css`: diseño responsivo con Grid/Flexbox, unidades relativas `rem`, `%` y `vw`; sin tamaños en `px`.
- `js/api.js`: **único módulo que realiza solicitudes HTTP**, maneja errores, autorización JWT y almacenamiento de sesión.
- `js/app.js`: navegación hash, DOM, formularios, vistas y eventos.
- `serve.py`: servidor estático y proxy local de `/api` a Flask. Evita problemas de CORS sin modificar el backend original.
- `localStorage`: sesión JWT y referencia del carrito abierto por usuario. Los ítems se persisten realmente en la API, de modo que el carrito también sobrevive a recargas. La sesión se limpia al cerrar sesión.
- Validación cliente: email con Regex, contraseña mínima de 8 caracteres, campos obligatorios, precios no negativos, cantidades enteras y límites de stock. El backend valida de nuevo.
- Los errores HTTP se muestran en pantalla; el catálogo vacío tiene estado específico.
- Los productos de la API **no contienen URLs de imágenes**; se muestran ilustraciones emoji en vez de inventar imágenes.
- Los precios se presentan con formato MXN como decisión visual; la API devuelve importes sin código de moneda. Cambia el formato en `money()` si tu tienda usa otra moneda.

## Integración con API

Base: `/api` (en el frontend); `serve.py` envía solicitudes a `http://127.0.0.1:5000/api`.

| Acción | Endpoint |
| --- | --- |
| Registro / login / logout | `POST /auth/register`, `/auth/login`, `/auth/logout` |
| Productos | `GET /products`, `GET /products/:id` |
| Crear / editar producto | `POST /products`, `PATCH /products/:id` |
| Carritos | `GET /carts`, `POST /carts` |
| Añadir / cambiar cantidad | `PUT /carts/:id/items/:productId` |
| Quitar producto | `DELETE /carts/:id/items/:productId` |
| Direcciones | `GET /users/:id/addresses`, `POST /users/:id/addresses` |
| Finalizar compra | `POST /carts/:id/checkout` |
| Ventas | `GET /invoices` |

**Importante:** el backend exige JWT incluso para listar productos; por eso el catálogo solicita login. El checkout necesita una dirección de facturación y una referencia de pago. Este es un proyecto académico: **no integra una pasarela de pago real**. La confirmación registra una venta y descuenta stock en el backend.

## Pruebas manuales sugeridas

1. Abrir inicio, registrar cuenta y entrar.
2. Comprobar catálogo vacío; entrar como administrador y crear producto.
3. Regresar como cliente; ver producto y añadirlo al carrito.
4. Modificar cantidad, eliminar producto y volver a agregarlo.
5. Crear dirección, confirmar compra y verificar pantalla de éxito.
6. Entrar como admin, revisar facturas y comprobar descuento de stock.
7. Probar email inválido, contraseña corta, stock insuficiente y backend apagado.

## Limitaciones

- El frontend no tiene pasarela de pago real, búsqueda avanzada ni subida de imágenes (no están disponibles en los endpoints proporcionados).
- El token se guarda en `localStorage` porque así lo exige el curso; en producción sería preferible estudiar cookies HttpOnly, CSP y protección contra XSS.
- La sesión expira según el JWT del backend (por defecto, 60 minutos); se necesita iniciar sesión nuevamente al expirar.
- Las pruebas de extremo a extremo requieren que el backend y su base de datos estén ejecutándose.
