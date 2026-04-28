from flask import render_template,Blueprint, request, jsonify
from models.quadtree import Quadtree
from models.puntos import Point
from models.recta import Rect

home_bp = Blueprint('home', __name__)

limite_pantalla = Rect(350, 300, 350, 300)
arbol_espacial = Quadtree(limite_pantalla, 4)

@home_bp.route('/')
def index():
    global arbol_espacial 
    arbol_espacial = Quadtree(limite_pantalla, 4)
    data = {"title": "Simulador Quadtree", "message": "¡Bienvenido!"}
    return render_template("index.html", data=data)

@home_bp.route('/insertar', methods=['POST'])
def insertar():
    datos = request.get_json()
    try:
        x = float(datos.get('x'))
        y = float(datos.get('y'))
        
        nuevo_punto = Point(x, y)
        exito = arbol_espacial.insertar(nuevo_punto)
        
        if exito:
            return jsonify({
                "status": "success",
                "cuadros": [
                    {"x": r.x, "y": r.y, "w": r.ancho, "h": r.alto} 
                    for r in arbol_espacial.obtener_todos_los_limites()
                ]
            })
        return jsonify({"status": "error", "message": "Fuera de límites"}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@home_bp.route('/limpiar', methods=['POST'])
def limpiar():
    global arbol_espacial 
    datos = request.get_json(silent=True)
    capacidad = datos.get('capacidad', 4) if datos else 4
    #arbol_espacial = Quadtree(limite_pantalla, 4) 
    arbol_espacial = Quadtree(limite_pantalla, int(capacidad))
    # Devolvemos el cuadro inicial para que el canvas no quede totalmente vacío
    return jsonify({
        "status": "success", 
        "message": "Árbol reiniciado",
        "cuadros": [{"x": 350, "y": 300, "w": 350, "h": 300}]
    })    
@home_bp.route('/obtener_limites', methods=['GET'])
def obtener_limites():
    try:
        limites = arbol_espacial.obtener_todos_los_limites()
        
        # Serializamos los objetos Rect a diccionarios para el JSON
        return jsonify({
            "status": "success",
            "cuadros": [
                {"x": r.x, "y": r.y, "w": r.ancho, "h": r.alto} 
                for r in limites
            ]
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400
