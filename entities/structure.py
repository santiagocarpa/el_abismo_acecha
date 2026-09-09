"""
entities/structure.py - Entidad de Estructura derivada de EntidadBase
"""

import pygame
from entities.entidad_base import EntidadBase

class Structure(EntidadBase):
    def __init__(self, x: float, y: float, struct_type: str = "fogata"):
        super().__init__(x, y, 48, 48, aplica_gravedad=False)
        self.struct_type = struct_type
        self.salud = 100
        self.light_radius = 180 if struct_type == "fogata" else 0
        self._create_sprite()

    def _create_sprite(self):
        self.image = pygame.Surface((self.ancho, self.alto), pygame.SRCALPHA)
        if self.struct_type == "fogata":
            pygame.draw.circle(self.image, (100, 60, 30), (24, 24), 16)
            pygame.draw.circle(self.image, (255, 140, 30), (24, 24), 10)
            pygame.draw.circle(self.image, (255, 230, 80), (24, 24), 5)
        elif self.struct_type == "muro_madera":
            pygame.draw.rect(self.image, (110, 70, 35), (4, 4, 40, 40), border_radius=4)
            pygame.draw.rect(self.image, (60, 40, 20), (4, 4, 40, 40), width=3, border_radius=4)
            pygame.draw.line(self.image, (60, 40, 20), (8, 24), (40, 24), 2)

    def actualizar_logica(self, dt: float):
        self.vx = 0.0
        self.vy = 0.0

    @property
    def pos(self) -> pygame.math.Vector2:
        return pygame.math.Vector2(self.x, self.y)

    def dibujar(self, pantalla: pygame.Surface, camara_offset: pygame.math.Vector2 = None):
        super().dibujar(pantalla, camara_offset)
