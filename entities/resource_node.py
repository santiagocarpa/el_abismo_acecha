"""
entities/resource_node.py - Entidad de Recurso derivada de EntidadBase
"""

import pygame
from entities.entidad_base import EntidadBase

class ResourceNode(EntidadBase):
    def __init__(self, x: float, y: float, resource_type: str = "arbol"):
        super().__init__(x, y, 44, 44, aplica_gravedad=False)
        self.resource_type = resource_type
        self.salud = 3 if resource_type == "arbol" else 5
        self.max_salud = self.salud
        self._create_sprite()

    def _create_sprite(self):
        self.image = pygame.Surface((self.ancho, self.alto), pygame.SRCALPHA)
        if self.resource_type == "arbol":
            pygame.draw.rect(self.image, (85, 55, 30), (18, 24, 8, 18))
            pygame.draw.circle(self.image, (30, 90, 45), (22, 18), 16)
        elif self.resource_type == "roca":
            pygame.draw.polygon(self.image, (110, 115, 110), [(8, 36), (22, 8), (38, 36)])
        else:
            pygame.draw.polygon(self.image, (130, 100, 90), [(6, 38), (22, 6), (40, 38)])
            pygame.draw.circle(self.image, (210, 140, 60), (22, 22), 5)

    def recibir_dano(self, cantidad: int = 1) -> bool:
        self.salud -= cantidad
        return self.salud <= 0

    def actualizar_logica(self, dt: float):
        self.vx = 0.0
        self.vy = 0.0

    @property
    def pos(self) -> pygame.math.Vector2:
        return pygame.math.Vector2(self.x, self.y)

    def dibujar(self, pantalla: pygame.Surface, camara_offset: pygame.math.Vector2 = None):
        super().dibujar(pantalla, camara_offset)
