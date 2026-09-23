"""
entities/enemy.py - Entidad Enemigo con Máquina de Estados (PATRULLA, PERSECUCION, ATAQUE)
"""

import pygame
import random
from config import COLOR_HEALTH_RED
from entities.entidad_base import EntidadBase

class Enemy(EntidadBase):
    def __init__(self, x: float, y: float):
        super().__init__(x, y, 32, 32, aplica_gravedad=False)
        self.speed = 120.0
        self.salud = 30
        self.dano = 15

        # Referencia al jugador objetivo
        self.target_player = None

        # Cooldown de ataque (ritmo de combate de 2 segundos)
        self.cooldown_ataque = 0.0

        # Attackbox para registrar el área del golpe
        self.attackbox = None

        # Estado inicial y Diccionario de Comportamientos en __init__
        self.estado = "PATRULLA"
        self.comportamientos = {
            "PATRULLA": self._estado_patrulla,
            "PERSECUCION": self._estado_persecucion,
            "ATAQUE": self._estado_ataque
        }

        # Variables para movimiento de patrullaje
        self.origen_x = x
        self.origen_y = y
        self.patrulla_timer = 0.0
        self.patrulla_dir = pygame.math.Vector2(0, 0)

        # Sprite del Enemigo
        self._create_sprite()

    def _create_sprite(self):
        self.image = pygame.Surface((self.ancho, self.alto), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (20, 15, 25), (16, 16), 14)
        pygame.draw.circle(self.image, COLOR_HEALTH_RED, (11, 12), 3)
        pygame.draw.circle(self.image, COLOR_HEALTH_RED, (21, 12), 3)

    def set_target_player(self, player):
        """Asigna el jugador objetivo para los comportamientos del enemigo."""
        self.target_player = player

    def set_target(self, player_pos):
        """Compatibilidad con asignación de posición."""
        pass

    def calcular_distancia_jugador(self, hitbox_jugador: pygame.Rect) -> float:
        """Calcula la distancia euclidiana entre el centro del Hitbox del enemigo y el centro del Hitbox del jugador."""
        if not hitbox_jugador:
            return 999999.0
        centro_enemigo = pygame.math.Vector2(self.hitbox.center)
        centro_jugador = pygame.math.Vector2(hitbox_jugador.center)
        return centro_enemigo.distance_to(centro_jugador)

    def _estado_patrulla(self, dt: float, target_player):
        """
        Método de Patrullaje:
        Regla: Si la distancia d <= 300 píxeles, cambia el estado a 'PERSECUCION'.
        """
        self.patrulla_timer -= dt
        if self.patrulla_timer <= 0:
            self.patrulla_timer = random.uniform(2.0, 4.0)
            ang_dir = random.uniform(0, 360)
            vec = pygame.math.Vector2(1, 0).rotate(ang_dir)
            self.patrulla_dir = vec * (self.speed * 0.4)

        self.vx = self.patrulla_dir.x
        self.vy = self.patrulla_dir.y

        if target_player and hasattr(target_player, 'hitbox'):
            d = self.calcular_distancia_jugador(target_player.hitbox)
            if d <= 300.0:
                self.estado = "PERSECUCION"

    def _estado_persecucion(self, dt: float, target_player):
        """
        Método de Persecución:
        Regla 1: Si d > 300 píxeles, vuelve a 'PATRULLA'.
        Regla 2: Si d <= 50 píxeles y cooldown_ataque <= 0, cambia a 'ATAQUE'.
        """
        if not target_player or not hasattr(target_player, 'hitbox'):
            self.estado = "PATRULLA"
            return

        d = self.calcular_distancia_jugador(target_player.hitbox)

        # Regla 1: Si el jugador se aleja y la distancia d > 300, vuelve a PATRULLA
        if d > 300.0:
            self.estado = "PATRULLA"
            return

        # Regla 2: Si la distancia d <= 50 y cooldown_ataque <= 0, cambia a ATAQUE
        if d <= 50.0 and self.cooldown_ataque <= 0.0:
            self.estado = "ATAQUE"
            self._estado_ataque(dt, target_player)
            return

        # Mover hacia la posición del jugador
        centro_jugador = pygame.math.Vector2(target_player.hitbox.center)
        centro_enemigo = pygame.math.Vector2(self.hitbox.center)
        direccion = (centro_jugador - centro_enemigo)

        if direccion.length() > 0:
            move_dir = direccion.normalize()
            self.vx = move_dir.x * self.speed
            self.vy = move_dir.y * self.speed

    def _estado_ataque(self, dt: float, target_player):
        """
        Método de Ataque:
        Instancia el Attackbox enemigo y automáticamente reinicia el temporizador: cooldown_ataque = 2.0.
        """
        self.vx = 0.0
        self.vy = 0.0

        # Instanciar el Attackbox alrededor del enemigo
        self.attackbox = self.hitbox.inflate(24, 24)

        # Infligir daño al jugador si el attackbox colisiona
        if target_player and hasattr(target_player, 'hitbox') and self.attackbox.colliderect(target_player.hitbox):
            target_player.recibir_dano(self.dano)

        # Reiniciar temporizador de cooldown a 2.0 segundos
        self.cooldown_ataque = 2.0

        # Retornar al estado de persecución
        self.estado = "PERSECUCION"

    def actualizar_logica(self, dt: float):
        # 1. Reducir el temporizador de cooldown en cada cuadro usando Delta Time: cooldown_ataque = cooldown_ataque - dt
        if self.cooldown_ataque > 0.0:
            self.cooldown_ataque -= dt
            if self.cooldown_ataque < 0.0:
                self.cooldown_ataque = 0.0

        # 2. Resetear el Attackbox del cuadro anterior
        self.attackbox = None

        # 3. Ejecutar el comportamiento según el estado del diccionario vinculador
        metodo_comportamiento = self.comportamientos.get(self.estado)
        if metodo_comportamiento:
            metodo_comportamiento(dt, self.target_player)

    @property
    def pos(self) -> pygame.math.Vector2:
        return pygame.math.Vector2(self.x, self.y)

    def dibujar(self, pantalla: pygame.Surface, camara_offset: pygame.math.Vector2 = None):
        super().dibujar(pantalla, camara_offset)
