"""
main.py - Punto de Entrada Principal para el videojuego "El Abismo Acecha"
"""

import sys
import os

# Asegurar que el directorio actual esté en el PATH de Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.engine import Engine

if __name__ == "__main__":
    print("Iniciando 'El Abismo Acecha'...")
    game_engine = Engine()
    game_engine.run()
