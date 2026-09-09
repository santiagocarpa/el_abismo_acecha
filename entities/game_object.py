"""
entities/game_object.py - Clase Base para todos los objetos del juego
"""

import pygame

class GameObject(pygame.sprite.Sprite):
    def __init__(self, x: float, y: float, width: int, height: int):
        super().__init__()
        self.pos = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(0, 0)
        self.width = width
        self.height = height

        # Crear superficie básica de representación por defecto
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))
        self.hitbox = self.rect.inflate(-4, -4)  # Hitbox ajustada para colisiones más precisas

    def update_position(self, dt: float):
        """Actualiza la posición del objeto usando Delta Time (dt)."""
        self.pos += self.velocity * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))
        self.hitbox.center = self.rect.center

    def update(self, dt: float):
        self.update_position(dt)

    def render(self, screen: pygame.Surface, camera_offset=pygame.math.Vector2(0, 0)):
        """Renderiza la entidad considerando el desplazamiento de la cámara."""
        render_pos = self.rect.topleft - camera_offset
        screen.blit(self.image, render_pos)
