const toggleBtn = document.getElementById('toggle-params');
const content = document.getElementById('params-content');
const arrow =document.querySelector('.arrow');

toggleBtn.addEventListener('click', () => {
    // Alterna la clase 'hidden' en el contenido
    content.classList.toggle('hidden');
    
    // Alterna la clase 'collapsed' en la flecha para que gire
    arrow.classList.toggle('collapsed');
});