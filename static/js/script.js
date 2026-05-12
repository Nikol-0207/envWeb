const toggleBtn = document.getElementById('toggle-params');
const content = document.getElementById('params-content');
const arrow =document.querySelector('.arrow');
const capacidadInput= document.getElementById('capacidad');

toggleBtn.addEventListener('click', () => {
    
    content.classList.toggle('hidden');
    arrow.classList.toggle('collapsed');
});

document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('canvas');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    const colorPicker = document.getElementById('color-picker');
    const countDisplay = document.getElementById('count');

    // Variables de estado
    let todosLosPuntos = [];
    let todasLasLineas = [];

    function redibujarTodo() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Dibujar Líneas de División
        ctx.lineWidth = 2;
        todasLasLineas.forEach(linea => {
            // Rojo para divisiones en X (Vertical), Azul para Y (Horizontal)
            ctx.strokeStyle = linea.eje === 0 ? "#ff4d4d" : "#4d79ff";
            ctx.beginPath();
            
            if (linea.eje === 0) {
                // Eje X: Línea vertical limitada por el rectángulo padre
                ctx.moveTo(linea.punto.x, linea.limite.y - linea.limite.h);
                ctx.lineTo(linea.punto.x, linea.limite.y + linea.limite.h);
            } else {
                // Eje Y: Línea horizontal limitada por el rectángulo padre
                ctx.moveTo(linea.limite.x - linea.limite.w, linea.punto.y);
                ctx.lineTo(linea.limite.x + linea.limite.w, linea.punto.y);
            }
            ctx.stroke();
        });

        todosLosPuntos.forEach(p => {
            ctx.save();
            ctx.shadowColor = p.color;
            ctx.shadowBlur = 15;
            ctx.fillStyle = p.color;
            ctx.beginPath();
            ctx.arc(p.x, p.y, 5, 0, Math.PI * 2);
            ctx.fill();
            ctx.restore();
            if (p.label) {
                ctx.save();
                ctx.fillStyle = "white"; 
                ctx.font = "bold 14px Arial";
                ctx.textAlign = "center";
               
                ctx.fillText(p.label, p.x, p.y - 12); 
                ctx.restore();
            }
        });
    }
    document.getElementById('btn-renombrar').addEventListener('click', () => {
    const oldNameEl = document.getElementById('old-name');
    const newNameEl = document.getElementById('new-name');

   
    const oldName = oldNameEl.value.trim();
    const newName = newNameEl.value.trim();
    if (!oldName || !newName){
        alert("⚠️ Por favor, complete ambos campos para renombrar el punto.");
        return; 
    }

    fetch('/renombrar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ oldName, newName })
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === "success") {
            //Actualizar el nombre en nuestra lista local de puntos
            const punto = todosLosPuntos.find(p => p.label === oldName);
            if (punto) {
                punto.label = newName;
                // Limpiar los inputs
                oldNameEl.value = "";
                newNameEl.value = "";
                
               
                redibujarTodo();
            }
        } else {
            alert("⚠️ No se encuentra el punto con ese nombre, ingrese una data que exista.");
    
        }
    })
    .catch(err => console.error("Error al renombrar:", err));
});
    const btnClear = document.getElementById('btn-clear');
     btnClear.addEventListener('click', () => {
    fetch('/limpiar', { method: 'POST' })
    .then(res => res.json())
    .then(data => {
        if (data.status === "success") {
            
            todosLosPuntos = [];
            todasLasLineas = [];
            
            //Resetear el contador visual
            if(countDisplay) countDisplay.innerText = "0";
            
            // Limpiar el dibujo del canvas
            redibujarTodo();
            
            console.log("Sistema reiniciado con éxito");
        }
    })
    .catch(err => console.error("Error al limpiar:", err));
});

    
    canvas.addEventListener('mousedown', (e) => {
        const rect = canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        fetch('/insertar', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ x: x, y: y })
        })
        .then(res => res.json())
        .then(data => {
            if (data.status === "success") {
              
                todosLosPuntos.push({ 
                x: x, 
                y: y, 
                color: colorPicker.value,
                label: data.punto_nuevo.label 
           });
                todasLasLineas = data.lineas; 
                
                if(countDisplay) countDisplay.innerText = todosLosPuntos.length;
                redibujarTodo();
            }
        })
        .catch(err => console.error("Error en la petición:", err));
    });
});






