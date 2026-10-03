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

  // Actualizar visualmente cantidades sin asumir lógica de carrito.
  document.querySelectorAll("[data-quantity]").forEach((input) => {
    const update = () => {
      const value = Math.max(1, parseInt(input.value, 10) || 1);
      input.value = value;
    };

    input.addEventListener("change", update);
  });

  // Actualizar indicadores visuales del carrito a partir del DOM.
  const updateCartIndicators = () => {
    const countElement = document.querySelector("[data-cart-count]");
    const cartItems = document.querySelectorAll("[data-cart-item]");

    if (countElement && cartItems.length) {
      let count = 0;

      cartItems.forEach((item) => {
        const quantity = item.querySelector("[data-quantity]");
        count += parseInt(quantity?.value, 10) || 0;
      });

      countElement.textContent = count;
      countElement.hidden = count === 0;
    }
  };

  updateCartIndicators();

  document.querySelectorAll("[data-quantity]").forEach((input) => {
    input.addEventListener("change", updateCartIndicators);
  });
});
