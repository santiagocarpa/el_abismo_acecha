"""
core/scene_manager.py - Gestor de Escenas y Transiciones Suaves (Fade In / Fade Out)
"""

import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT

class SceneManager:
    def __init__(self, engine):
        self.engine = engine
        self.scenes = {}
        self.current_scene = None
        self.scene_stack = []

        # Estado de Transición (Fade)
        self.is_transitioning = False
        self.transition_speed = 400.0  # Cambio de Alpha por segundo
        self.fade_alpha = 0.0
        self.fade_mode = None  # 'out' (oscureciendo) o 'in' (aclarando)
        self.next_scene_name = None
        self.next_scene_data = None

        # Superficie para el efecto Fade
        self.fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.fade_surface.fill((0, 0, 0))

    def register_scene(self, name: str, scene_instance):
        """Registra una escena en el diccionario por nombre."""
        self.scenes[name] = scene_instance

    def change_scene(self, name: str, data=None, with_fade: bool = True):
        """Cambia a una escena registrada con o sin transición suave."""
        if name not in self.scenes:
            raise ValueError(f"Escena '{name}' no registrada en SceneManager.")

        if with_fade:
            self.is_transitioning = True
            self.fade_mode = 'out'
            self.fade_alpha = 0.0
            self.next_scene_name = name
            self.next_scene_data = data
        else:
            self._switch_to_scene(name, data)

    def _switch_to_scene(self, name: str, data=None):
        if self.current_scene:
            self.current_scene.on_exit()
        self.current_scene = self.scenes[name]
        self.current_scene.on_enter(data)

    def push_scene(self, name: str, data=None):
        """Superpone una escena sobre la actual (ej: Pausa o Crafteo)."""
        if self.current_scene:
            self.scene_stack.append(self.current_scene)
        self.current_scene = self.scenes[name]
        self.current_scene.on_enter(data)

    def pop_scene(self):
        """Retira la escena superior y vuelve a la escena previa."""
        if self.scene_stack:
            if self.current_scene:
                self.current_scene.on_exit()
            self.current_scene = self.scene_stack.pop()

    def handle_events(self, events):
        if not self.is_transitioning and self.current_scene:
            self.current_scene.handle_events(events)

    def update(self, dt: float):
        # Actualización de lógica de la escena activa
        if self.current_scene:
            self.current_scene.update(dt)

        # Actualización de la matemática de transición Fade
        if self.is_transitioning:
            if self.fade_mode == 'out':
                self.fade_alpha += self.transition_speed * dt
                if self.fade_alpha >= 255.0:
                    self.fade_alpha = 255.0
                    self._switch_to_scene(self.next_scene_name, self.next_scene_data)
                    self.fade_mode = 'in'
            elif self.fade_mode == 'in':
                self.fade_alpha -= self.transition_speed * dt
                if self.fade_alpha <= 0.0:
                    self.fade_alpha = 0.0
                    self.is_transitioning = False
                    self.fade_mode = None

    def render(self, screen: pygame.Surface):
        # Renderiza la pila de escenas si aplica o la escena actual
        for stacked in self.scene_stack:
            stacked.render(screen)

        if self.current_scene:
            self.current_scene.render(screen)

        # Renderiza la capa de transición Alpha
        if self.is_transitioning and self.fade_alpha > 0:
            self.fade_surface.set_alpha(int(self.fade_alpha))
            screen.blit(self.fade_surface, (0, 0))
