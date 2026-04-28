# 🌳 Visualización espacial de Quadtree (2D)
![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Flask](https://img.shields.io/badge/Framework-Flask-lightgrey.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)


![EStructura](https://i.blogs.es/c3c00f/quadtree_arbol-20-1-/450_1000.webp)
Este proyecto es un simulador interactivo de una estructura de datos **Quadtree**, diseñada para la organización eficiente de datos espaciales. Permite visualizar en tiempo real cómo se subdivide el plano bidimensional a medida que se insertan puntos, optimizando la búsqueda y el almacenamiento.
## ¿Qué es un Quadtree?
Un quadtree (o árbol cuaternario) es una estructura de datos jerárquica en forma de árbol diseñada para dividir un espacio bidimensional (2D) subdividiéndolo recursivamente en cuatro cuadrantes o regiones. Cada nodo interno tiene exactamente cuatro hijos (noroeste, noreste, suroeste, sureste), lo que permite organizar datos espaciales (puntos, imágenes) de manera eficiente para búsquedas rápidas. 

## 🚀 Características

- **Visualización Dinámica:** Inserción de puntos mediante clics en un Canvas de HTML5.
- **Capacidad Configurable:** Ajuste en tiempo real de la capacidad de los nodos (threshold) sin recargar la página.
- **Panel de Parámetros:** Sidebar colapsable para controlar la capacidad, el color y ver las coordenadas de los nodos.

## 🛠️ Tecnologías Utilizadas

- **Backend:** Python 3.10, Flask.
- **Frontend:** JavaScript , CSS, HTML.
- **Contenerización:** Docker & Docker Compose.
- **Entorno de Desarrollo:** Linux Mint / Ubuntu.

