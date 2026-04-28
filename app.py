
from flask import Flask
from controllers.home_controller import index, insertar, limpiar, obtener_limites

app = Flask(__name__)

# Registrar rutas
app.add_url_rule("/", view_func=index)

app.add_url_rule("/insertar", view_func=insertar, methods=["POST"])
app.add_url_rule("/limpiar", view_func=limpiar, methods=["POST"])
app.add_url_rule("/obtener_limites", view_func=obtener_limites, methods=["GET"])

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)