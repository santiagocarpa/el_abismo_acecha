"""
scenes/base_scene.py - Clase Base Abstracta para todas las escenas
"""

import pygame

class BaseScene:
    def __init__(self, scene_manager):
        self.scene_manager = scene_manager

    def on_enter(self, data=None):
        """Llamado cuando la escena se vuelve activa."""
        pass

    def on_exit(self):
        """Llamado cuando la escena deja de estar activa."""
        pass

    def handle_events(self, events):
        """Procesa la lista de eventos de Pygame."""
        pass

    def update(self, dt: float):
        """Actualiza la lógica interna de la escena en función de delta time (dt en segundos)."""
        pass

    def render(self, screen: pygame.Surface):
        """Renderiza los elementos gráficos en la superficie principal de la pantalla."""
        pass
