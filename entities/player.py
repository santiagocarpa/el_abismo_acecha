"""
entities/player.py - Entidad del Jugador con Muerte (HP=0) y Sistema de Agotamiento de Estamina
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
        self.is_dead = False

        # Atributos de Estamina y Agotamiento
        self.stamina = PLAYER_MAX_STAMINA
        self.stamina_max = PLAYER_MAX_STAMINA
        self.is_sprinting = False
        self.is_exhausted = False  # Bandera de cansancio cuando la estamina llega a 0

        # Equipamiento y Daño de Ataque
        self.dano_base = 10
        self.tiene_espada = False

        # Referencia al Inventario (se asigna en GameScene)
        self.inventory = None

        # Sprite del Jugador
        self._create_sprite()

    def _create_sprite(self):
        self.image = pygame.Surface((self.ancho, self.alto), pygame.SRCALPHA)
        # Cuerpo del jugador
        pygame.draw.circle(self.image, (60, 140, 90), (self.ancho // 2, self.alto // 2), 14)
        pygame.draw.circle(self.image, COLOR_TEXT_GOLD, (self.ancho // 2, self.alto // 2), 14, width=2)
        # Cabeza / Dirección
        pygame.draw.circle(self.image, (220, 220, 220), (self.ancho // 2, self.alto // 2 - 6), 5)

    def recibir_dano(self, cantidad: int):
        """Aplica daño al jugador y verifica estado de muerte."""
        if self.is_dead:
            return

        self.salud -= cantidad
        if self.salud <= 0:
            self.salud = 0
            self.is_dead = True

    def handle_input(self):
        if self.is_dead:
            self.vx = 0.0
            self.vy = 0.0
            return

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

        # Sprint: Solo permitido si NO está agotado y presiona SHIFT
        want_sprint = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
        if want_sprint and not self.is_exhausted and move_vec.length() > 0 and self.stamina > 0.0:
            self.is_sprinting = True
        else:
            self.is_sprinting = False

        speed_mult = PLAYER_SPRINT_MULT if self.is_sprinting else 1.0
        
        self.vx = move_vec.x * (PLAYER_SPEED * speed_mult)
        self.vy = move_vec.y * (PLAYER_SPEED * speed_mult)

    def actualizar_logica(self, dt: float):
        if self.is_dead:
            return

        self.handle_input()

        # Lógica de Consumo y Recuperación de Estamina
        if self.is_sprinting:
            self.stamina -= 45.0 * dt
            if self.stamina <= 0.0:
                self.stamina = 0.0
                self.is_sprinting = False
                self.is_exhausted = True  # ¡El personaje se agota completamente!
        else:
            self.stamina = min(self.stamina_max, self.stamina + PLAYER_STAMINA_REGEN * dt)
            # Recuperar de agotamiento solo cuando la estamina supera el 35%
            if self.is_exhausted and self.stamina >= 35.0:
                self.is_exhausted = False

        # Clamping dentro de los bordes del mapa del mundo
        self.x = max(16.0, min(WORLD_WIDTH - 16.0, self.x))
        self.y = max(16.0, min(WORLD_HEIGHT - 16.0, self.y))

    @property
    def pos(self) -> pygame.math.Vector2:
        return pygame.math.Vector2(self.x, self.y)

    def dibujar(self, pantalla: pygame.Surface, camara_offset: pygame.math.Vector2 = None):
        super().dibujar(pantalla, camara_offset)
