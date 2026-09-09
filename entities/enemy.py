"""
entities/enemy.py - Entidad Enemigo derivada de EntidadBase
"""

import pygame
from config import COLOR_HEALTH_RED
from entities.entidad_base import EntidadBase

class Enemy(EntidadBase):
    def __init__(self, x: float, y: float):
        super().__init__(x, y, 32, 32, aplica_gravedad=False)
        self.speed = 130.0
        self.salud = 30
        self.dano = 15
        self.attack_cooldown = 0.0
        self.target_pos = None

        self._create_sprite()

    def _create_sprite(self):
        self.image = pygame.Surface((self.ancho, self.alto), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (20, 15, 25), (16, 16), 14)
        pygame.draw.circle(self.image, COLOR_HEALTH_RED, (11, 12), 3)
        pygame.draw.circle(self.image, COLOR_HEALTH_RED, (21, 12), 3)

    def set_target(self, player_pos: pygame.math.Vector2):
        self.target_pos = player_pos

    def actualizar_logica(self, dt: float):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt

        if self.target_pos:
            direction = self.target_pos - pygame.math.Vector2(self.x, self.y)
            distance = direction.length()

            if distance > 10.0:
                move_dir = direction.normalize()
                self.vx = move_dir.x * self.speed
                self.vy = move_dir.y * self.speed
            else:
                self.vx = 0.0
                self.vy = 0.0

    @property
    def pos(self) -> pygame.math.Vector2:
        return pygame.math.Vector2(self.x, self.y)

    def dibujar(self, pantalla: pygame.Surface, camara_offset: pygame.math.Vector2 = None):
        super().dibujar(pantalla, camara_offset)
