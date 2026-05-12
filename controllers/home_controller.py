from flask import render_template,Blueprint, request, jsonify
from models.kdtree import Kdtree
from models.puntos import Point
from models.recta import Rect
import string
home_bp = Blueprint('home', __name__)
limite_inicial = Rect(350, 300, 350, 300)
arbol = Kdtree()
#Método auxiliar para etiquetar los puntosimport string
contador_puntos = 0
def generar_etiqueta(indice):
    letras = string.ascii_uppercase # "ABC...Z"
    ciclo = indice // 26
    letra = letras[indice % 26]
    if ciclo == 0:
        return letra
    else:
        return f"{letra}{ciclo}"
    
#Endpoints
@home_bp.route('/')
def index():
    data = {"title": "Simulador Quadtree", "message": "¡Bienvenido!"}
    return render_template("index.html", data=data)

@home_bp.route('/insertar', method=['POST'])
def insertar():
    global contador_puntos
    etiqueta = generar_etiqueta(contador_puntos)
    contador_puntos += 1
    data = request.get_json()
    nuevo_punto = Point(data['x'], data['y'], data=etiqueta)

    arbol.insertar(nuevo_punto)

    lineas_para_js = []
    exportar_lineas_recursivo(arbol.raiz, limite_inicial, lineas_para_js)
    
    return jsonify({
        "status": "success",
        "lineas": lineas_para_js,
        "punto_nuevo": {"x": data['x'], "y": data['y'], "label": etiqueta}
    })


def exportar_lineas_recursivo(nodo, rect_actual, lista):
    if nodo is None:
        return
    
    lista.append({
        "punto": {"x": nodo.punto.x, "y": nodo.punto.y},
        "eje": nodo.eje,
        "limite": {
            "x": rect_actual.x, 
            "y": rect_actual.y, 
            "w": rect_actual.ancho, 
            "h": rect_actual.alto
        }
    })
    
    rect_izq, rect_der = rect_actual.partir(nodo.punto, nodo.eje)
    
    exportar_lineas_recursivo(nodo.izq, rect_izq, lista)
    exportar_lineas_recursivo(nodo.der, rect_der, lista)

@home_bp.route('/limpiar', methods=['POST'])
def limpiar():
     global arbol
     arbol= Kdtree()
     contador_puntos=0
     return jsonify({"status": "success", "message": "Árbol reiniciado"})  

@home_bp.route('/renombrar', methods=['POST'])
def renombrar():
    data = request.get_json()
    nombre_antiguo = data.get('oldName')
    nombre_nuevo = data.get('newName')
    
    # Buscamos el punto en el árbol y cambiamos su data
    punto_encontrado = buscar_y_renombrar_recursivo(arbol.raiz, nombre_antiguo, nombre_nuevo)
    
    if punto_encontrado:
        return jsonify({"status": "success", "message": f"Punto {nombre_antiguo} renombrado a {nombre_nuevo}"})
    else:
        return jsonify({"status": "error", "message": "Punto no encontrado"}), 404

def buscar_y_renombrar_recursivo(nodo, antiguo, nuevo):
    if nodo is None:
        return False
    
    # Si el dato coincide, lo renombramos
    if nodo.punto.data == antiguo:
        nodo.punto.data = nuevo # Usamos el setter de la clase Point
        return True
    
   
    return buscar_y_renombrar_recursivo(nodo.izq, antiguo, nuevo) or \
           buscar_y_renombrar_recursivo(nodo.der, antiguo, nuevo)

@home_bp.route('/buscar_por_nombre', methods=['POST'])
def buscar_por_nombre():
    data = request.get_json()
    nombre_buscado = data.get('nombre')
    
    # Buscamos el punto en el árbol
    punto_encontrado = buscar_punto_recursivo(arbol.raiz, nombre_buscado)
    
    if punto_encontrado:
        return jsonify({"status": "success", "x": punto_encontrado.x, "y": punto_encontrado.y})
    return jsonify({"status": "error"}), 404

def buscar_punto_recursivo(nodo, nombre):
    if nodo is None:
        return None
    
    # Si encontramos la etiqueta en el atributo 'data'
    if nodo.punto.data == nombre:
        return nodo.punto
    
    # Buscamos en ambos lados
    izq = buscar_punto_recursivo(nodo.izq, nombre)
    if izq: return izq
    
    return buscar_punto_recursivo(nodo.der, nombre)

@home_bp.route('/buscar_vecino', methods=['POST'])
def buscar_vecino():
    data = request.get_json()
    coords_raw = data.get('coords') # Viene como "123,134"
    
    try:
        x_buscada, y_buscada = map(float, coords_raw.split(','))
        
        punto_cercano, distancia = arbol.buscar_mas_cercano(x_buscada, y_buscada)
        
        if punto_cercano:
            return jsonify({
                "status": "success",
                "label": punto_cercano.data,
                "x": punto_cercano.x,
                "y": punto_cercano.y
            })
        return jsonify({"status": "error", "message": "Árbol vacío"}), 404
    except:
        return jsonify({"status": "error", "message": "Formato incorrecto (use X,Y)"}), 400