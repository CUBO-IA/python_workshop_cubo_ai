document.addEventListener("DOMContentLoaded", () => {
  // Confirmar acciones peligrosas o irreversibles.
  document.querySelectorAll("[data-confirm]").forEach((element) => {
    element.addEventListener("click", (event) => {
      const message = element.dataset.confirm;

      if (message && !window.confirm(message)) {
        event.preventDefault();
      }
    });
  });

  // Menú responsive.
  const menuButton = document.querySelector("[data-menu-toggle]");
  const menu = document.querySelector("[data-menu]");

  if (menuButton && menu) {
    menuButton.addEventListener("click", () => {
      const isOpen = menu.classList.toggle("is-open");
      menuButton.setAttribute("aria-expanded", String(isOpen));
    });
  }

  // Evitar cantidades invalidas en los inputs numericos.
  const normalizeQuantity = (input) => {
    const value = Math.max(1, parseInt(input.value, 10) || 1);
    input.value = value;
    return value;
  };

  const quantityInputs = document.querySelectorAll("[data-quantity]");
  quantityInputs.forEach((input) => {
    input.addEventListener("change", () => normalizeQuantity(input));
  });

  // Contador del carrito en el encabezado.
  const cartLink = document.querySelector(".cart-link");
  const cartItems = document.querySelectorAll("[data-cart-item]");

  if (cartLink) {
    let countElement = document.querySelector("[data-cart-count]");

    if (!countElement) {
      countElement = document.createElement("span");
      countElement.className = "cart-count";
      countElement.setAttribute("data-cart-count", "");
      countElement.hidden = true;
      cartLink.appendChild(countElement);
    }

    const updateCartCount = () => {
      // Solo el carrito detailed conoce las cantidades reales.
      if (!cartItems.length) {
        return;
      }

      let count = 0;

      cartItems.forEach((item) => {
        const input = item.querySelector("[data-quantity]");
        count += parseInt(input?.value, 10) || 0;
      });

      countElement.textContent = count;
      countElement.hidden = count === 0;
    };

    quantityInputs.forEach((input) => {
      input.addEventListener("change", updateCartCount);
    });

    updateCartCount();
  }
});
