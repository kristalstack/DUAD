// Local persistence per account. The API remains authoritative for stock and checkout.
const prefix = "lyfter_cart_";
export const cartKey = (userId) => `${prefix}${userId}`;

export function readStoredCart(userId) {
  if (userId == null) return null;
  try {
    const raw = localStorage.getItem(cartKey(userId));
    const cart = raw ? JSON.parse(raw) : null;
    return cart && typeof cart === "object" && Number.isInteger(Number(cart.id))
      ? cart : null;
  } catch {
    localStorage.removeItem(cartKey(userId));
    return null;
  }
}

export function storeCart(userId, cart) {
  if (userId == null) return;
  if (!cart || cart.status !== "open") {
    localStorage.removeItem(cartKey(userId));
    return;
  }
  localStorage.setItem(cartKey(userId), JSON.stringify(cart));
}

export function clearStoredCart(userId) {
  if (userId != null) localStorage.removeItem(cartKey(userId));
}
