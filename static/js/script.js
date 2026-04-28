const toggleBtn = document.getElementById('toggle-params');
const content = document.getElementById('params-content');
const arrow =document.querySelector('.arrow');
const capacidadInput= document.getElementById('capacidad');

toggleBtn.addEventListener('click', () => {
    // Alterna la clase 'hidden' en el contenido
    content.classList.toggle('hidden');
    
    // Alterna la clase 'collapsed' en la flecha para que gire
    arrow.classList.toggle('collapsed');
});

document.addEventListener('DOMContentLoaded', () => {
    
    const canvas = document.getElementById('canvas');
    if (!canvas) {
        console.error("¡ERROR! No se encontró el elemento con ID 'canvas'");
        return;
    }
    const ctx = canvas.getContext('2d');
    const colorPicker = document.getElementById('color-picker');
    const countDisplay = document.getElementById('count');
    const btnClear = document.getElementById('btn-clear');

    let todosLosPuntos = [];
    let todosLosCuadros = [];

    function redibujarTodo() {
        console.log("Redibujando... Cuadros:", todosLosCuadros.length, "Puntos:", todosLosPuntos.length);
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Dibujar Cuadrículas
        ctx.strokeStyle = "#dce2df"; 
        ctx.lineWidth = 1;
        todosLosCuadros.forEach(r => {
            ctx.strokeRect(r.x - r.w, r.y - r.h, r.w * 2, r.h * 2);
        });

        // Dibujar Puntos
        todosLosPuntos.forEach(p => {
            ctx.save();

            ctx.shadowColor = p.color; // Color del resplandor
            ctx.shadowBlur = 15;        
            ctx.shadowOffsetX = 0;
             ctx.shadowOffsetY = 0;

            ctx.fillStyle = p.color;
            ctx.beginPath();
            ctx.arc(p.x, p.y, 4, 0, Math.PI * 2);
            ctx.fill();

           // ctx.restore();
        });
    }

    canvas.addEventListener('mousedown', (e) => {
        const rect = canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        console.log(`Clic detectado en: ${x}, ${y}`);

        fetch('/insertar', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ x: x, y: y })
        })
        .then(res => res.json())
        .then(data => {
            console.log("Respuesta de Flask:", data);
            if (data.status === "success") {
                todosLosPuntos.push({ x: x, y: y, color: colorPicker.value });
                todosLosCuadros = data.cuadros;
                if(countDisplay) countDisplay.innerText = todosLosPuntos.length;
                redibujarTodo();
            }
        })
        .catch(err => console.error("Error en Fetch:", err));
    }); 
       
        
     const btnMostrarLimites = document.getElementById('btn-mostrar-limites');
const infoLimites = document.getElementById('info-limites');

btnMostrarLimites.addEventListener('click', () => {
    fetch('/obtener_limites')
    .then(res => res.json())
    .then(data => {
        if (data.status === "success") {
            // Actualizar el dibujo en el Canvas
            todosLosCuadros = data.cuadros;
            redibujarTodo();
            
            //Mostrar la info debajo del botón
            // Limpiamos el contenido previo
            infoLimites.innerHTML = `<h3>Nodos detectados: ${data.cuadros.length}</h3>`;
            
            const lista = document.createElement('ul');
            data.cuadros.forEach((r, index) => {
                const item = document.createElement('li');
                item.style.marginBottom = "5px";
                item.innerHTML = `<strong>Nodo ${index + 1}:</strong> Centro(${r.x}, ${r.y}) | Radio(${r.w}x${r.h})`;
                lista.appendChild(item);
            });
            
            infoLimites.appendChild(lista);
        }
    })
    .catch(err => {
        infoLimites.innerHTML = `<p style="color: red;">Error: No se pudo conectar con el servidor.</p>`;
    });
});

    btnClear.addEventListener('click', () => {
          todosLosPuntos = [];
          todosLosCuadros = [];
           pointsCount = 0;
          if(countDisplay) countDisplay.innerText = 0;

          ctx.clearRect(0, 0, canvas.width, canvas.height);
           fetch('/limpiar', { method: 'POST' })
           .then(res => res.json())
           .then(data => {
          todosLosCuadros = data.cuadros;
           redibujarTodo(); // Esto dibujará solo el rectángulo exterior inicial
           if(document.getElementById('info-limites')) {
            document.getElementById('info-limites').innerHTML = "";
        }
      }); 
        console.log("Lienzo limpio");
          
    });

    capacidadInput.addEventListener('change', () => {
    let nuevaCapacidad = parseInt(capacidadInput.value);

    
    if (isNaN(nuevaCapacidad) || nuevaCapacidad < 1) {
        alert("La capacidad debe ser al menos 1");
        capacidadInput.value = 4; // Reset visual
        return;
    }

    // Enviamos la orden de reinicio con la nueva capacidad
    fetch('/limpiar', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ capacidad: nuevaCapacidad })
    })
    .then(res => res.json())
    .then(data => {
        // Limpiamos todo el estado local
        todosLosPuntos = [];
        todosLosCuadros = data.cuadros;
        pointsCount = 0;
        if(countDisplay) countDisplay.innerText = 0;
        
        // Redibujamos el lienzo (ahora solo quedará el cuadro raíz)
        redibujarTodo();
        console.log("Árbol reiniciado con capacidad:", nuevaCapacidad);
    });
});
});




