#!/usr/bin/env python3
"""
Fraseesencial - Punto de entrada de la aplicación
"""
from app import create_app

# Crear la aplicación (esto expone 'app' para flask shell)
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
