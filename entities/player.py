"""
entities/player.py - Entidad del Jugador derivada de EntidadBase
"""

import pygame
from config import (PLAYER_SPEED, PLAYER_MAX_HP, PLAYER_MAX_STAMINA, 
                    PLAYER_STAMINA_REGEN, PLAYER_SPRINT_MULT, PLAYER_SIZE,
                    WORLD_WIDTH, WORLD_HEIGHT, COLOR_TEXT_GOLD)
from entities.entidad_base import EntidadBase

class Player(EntidadBase):
    def __init__(self, x: float, y: float):
        super().__init__(x, y, PLAYER_SIZE[0], PLAYER_SIZE[1], aplica_gravedad=False)

        # Atributos de Estado y Salud
        self.salud = PLAYER_MAX_HP
        self.salud_max = PLAYER_MAX_HP
        self.stamina = PLAYER_MAX_STAMINA
        self.stamina_max = PLAYER_MAX_STAMINA
        self.is_sprinting = False

        # Generar gráfico temporal estilo Pixel Art para el Jugador
        self._create_sprite()

    def _create_sprite(self):
        self.image = pygame.Surface((self.ancho, self.alto), pygame.SRCALPHA)
        # Cuerpo del jugador
        pygame.draw.circle(self.image, (60, 140, 90), (self.ancho // 2, self.alto // 2), 14)
        pygame.draw.circle(self.image, COLOR_TEXT_GOLD, (self.ancho // 2, self.alto // 2), 14, width=2)
        # Cabeza / Dirección
        pygame.draw.circle(self.image, (220, 220, 220), (self.ancho // 2, self.alto // 2 - 6), 5)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        dx, dy = 0.0, 0.0

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= 1.0
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += 1.0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= 1.0
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += 1.0

        move_vec = pygame.math.Vector2(dx, dy)
        if move_vec.length() > 0:
            move_vec = move_vec.normalize()

        # Sprint (Tecla SHIFT)
        self.is_sprinting = keys[pygame.K_LSHIFT] and self.stamina > 5.0 and move_vec.length() > 0
        speed_mult = PLAYER_SPRINT_MULT if self.is_sprinting else 1.0
        
        # Asignar a los vectores vx y vy de EntidadBase
        self.vx = move_vec.x * (PLAYER_SPEED * speed_mult)
        self.vy = move_vec.y * (PLAYER_SPEED * speed_mult)

    def actualizar_logica(self, dt: float):
        self.handle_input()

        # Gestión de Stamina
        if self.is_sprinting:
            self.stamina = max(0.0, self.stamina - 35.0 * dt)
        else:
            self.stamina = min(self.stamina_max, self.stamina + PLAYER_STAMINA_REGEN * dt)

        # Clamping dentro de los bordes del mapa del mundo
        self.x = max(16.0, min(WORLD_WIDTH - 16.0, self.x))
        self.y = max(16.0, min(WORLD_HEIGHT - 16.0, self.y))

    @property
    def pos(self) -> pygame.math.Vector2:
        return pygame.math.Vector2(self.x, self.y)

    def dibujar(self, pantalla: pygame.Surface, camara_offset: pygame.math.Vector2 = None):
        super().dibujar(pantalla, camara_offset)
