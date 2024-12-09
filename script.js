// Función para mostrar elementos al hacer scroll
window.addEventListener('scroll', () => {
    const elements = document.querySelectorAll('.card');
    elements.forEach((element) => {
      const position = element.getBoundingClientRect();
      if (position.top < window.innerHeight && position.bottom >= 0) {
        element.classList.add('visible');
      } else {
        element.classList.remove('visible');
      }
    });
  });
  
  // CSS para animación (aplica opacidad 0 a los elementos)
  document.styleSheets[0].insertRule(`
    .card {
      opacity: 0;
      transition: opacity 1s ease-out;
    }
  `, 0);
  
  // CSS para animación (hace visibles los elementos cuando están en la ventana)
  document.styleSheets[0].insertRule(`
    .card.visible {
      opacity: 1;
    }
  `, 0);
  