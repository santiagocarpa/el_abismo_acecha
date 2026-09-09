"""
scenes/game_scene.py - Escena Principal de Juego adaptada a EntidadBase
"""

import pygame
import random
from config import (SCREEN_WIDTH, SCREEN_HEIGHT, WORLD_WIDTH, WORLD_HEIGHT, 
                    TILE_SIZE, COLOR_DARK_GREEN)
from scenes.base_scene import BaseScene
from entities.player import Player
from entities.resource_node import ResourceNode
from entities.structure import Structure
from entities.enemy import Enemy
from systems.day_night import DayNightSystem
from ui.hud import HUD
from core.database import DatabaseManager

class GameScene(BaseScene):
    def __init__(self, scene_manager):
        super().__init__(scene_manager)
        self.db = DatabaseManager()
        self.hud = HUD()

        self.player = None
        self.camera_offset = pygame.math.Vector2(0, 0)
        self.day_night = DayNightSystem(cycle_duration=90.0)

        self.resource_nodes = []
        self.structures = []
        self.enemies = []
        self.partida_id = None
        self.terrain_surface = None

    def on_enter(self, data=None):
        if data and "partida_id" in data:
            self.partida_id = data["partida_id"]
            datos_partida = self.db.cargar_partida(self.partida_id)
            if datos_partida:
                self.player = Player(datos_partida["pos_x"], datos_partida["pos_y"])
                self.player.salud = datos_partida["salud_actual"]
                self.player.stamina = datos_partida["stamina_actual"]
                self.day_night.day_number = datos_partida["dia_actual"]
                self.day_night.time = datos_partida["tiempo_dia"]
            else:
                self.player = Player(WORLD_WIDTH // 2, WORLD_HEIGHT // 2)
        else:
            self.player = Player(WORLD_WIDTH // 2, WORLD_HEIGHT // 2)

        self._generate_terrain()
        self._populate_world()

    def _generate_terrain(self):
        self.terrain_surface = pygame.Surface((WORLD_WIDTH, WORLD_HEIGHT))
        self.terrain_surface.fill(COLOR_DARK_GREEN)
        random.seed(42)
        for y in range(0, WORLD_HEIGHT, TILE_SIZE):
            for x in range(0, WORLD_WIDTH, TILE_SIZE):
                color_variant = (
                    max(15, COLOR_DARK_GREEN[0] + random.randint(-4, 6)),
                    max(30, COLOR_DARK_GREEN[1] + random.randint(-6, 8)),
                    max(20, COLOR_DARK_GREEN[2] + random.randint(-4, 6))
                )
                pygame.draw.rect(self.terrain_surface, color_variant, (x, y, TILE_SIZE, TILE_SIZE))
                pygame.draw.rect(self.terrain_surface, (20, 40, 26), (x, y, TILE_SIZE, TILE_SIZE), width=1)

    def _populate_world(self):
        self.resource_nodes.clear()
        self.structures.clear()
        self.enemies.clear()

        random.seed(100)
        for _ in range(80):
            rx = random.randint(100, WORLD_WIDTH - 100)
            ry = random.randint(100, WORLD_HEIGHT - 100)
            self.resource_nodes.append(ResourceNode(rx, ry, "arbol"))

        for _ in range(35):
            rx = random.randint(100, WORLD_WIDTH - 100)
            ry = random.randint(100, WORLD_HEIGHT - 100)
            self.resource_nodes.append(ResourceNode(rx, ry, "roca"))

        self.structures.append(Structure(WORLD_WIDTH // 2 + 60, WORLD_HEIGHT // 2 + 60, "fogata"))

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.scene_manager.push_scene("pause")
                elif event.key == pygame.K_f:
                    self._interact()
                elif event.key == pygame.K_c:
                    self.structures.append(Structure(self.player.x + 30, self.player.y, "fogata"))

    def _interact(self):
        for node in list(self.resource_nodes):
            dist = (self.player.pos - node.pos).length()
            if dist < 50.0:
                destruido = node.recibir_dano(1)
                if destruido:
                    self.resource_nodes.remove(node)
                break

    def update(self, dt: float):
        self.day_night.update(dt)

        # Actualización de Entidades heredadas de EntidadBase mediante actualizar()
        self.player.actualizar(dt, obstaculos=self.structures)

        if self.player.salud <= 0:
            self.scene_manager.change_scene("game_over")
            return

        if self.day_night.get_phase_name().startswith("Noche") and len(self.enemies) < 5:
            if random.random() < 0.02:
                spawn_x = self.player.x + random.choice([-400, 400])
                spawn_y = self.player.y + random.choice([-300, 300])
                self.enemies.append(Enemy(spawn_x, spawn_y))

        for enemy in list(self.enemies):
            enemy.set_target(self.player.pos)
            enemy.actualizar(dt, obstaculos=self.structures)
            if enemy.hitbox.colliderect(self.player.hitbox) and enemy.attack_cooldown <= 0:
                self.player.salud -= enemy.dano
                enemy.attack_cooldown = 1.2

        for node in self.resource_nodes:
            node.actualizar(dt)

        for struct in self.structures:
            struct.actualizar(dt)

        # Cámara centrada en el jugador
        self.camera_offset.x = self.player.x - SCREEN_WIDTH // 2
        self.camera_offset.y = self.player.y - SCREEN_HEIGHT // 2

    def render(self, screen: pygame.Surface):
        screen.blit(self.terrain_surface, (-self.camera_offset.x, -self.camera_offset.y))

        # Renderizar Entidades heredadas de EntidadBase mediante dibujar()
        for node in self.resource_nodes:
            node.dibujar(screen, self.camera_offset)

        for struct in self.structures:
            struct.dibujar(screen, self.camera_offset)

        for enemy in self.enemies:
            enemy.dibujar(screen, self.camera_offset)

        self.player.dibujar(screen, self.camera_offset)

        # Fuentes de luz (Fogatas)
        light_sources = []
        for struct in self.structures:
            if struct.light_radius > 0:
                screen_pos = (int(struct.x - self.camera_offset.x), int(struct.y - self.camera_offset.y))
                light_sources.append((screen_pos, struct.light_radius))

        player_screen_pos = (int(self.player.x - self.camera_offset.x), int(self.player.y - self.camera_offset.y))
        light_sources.append((player_screen_pos, 100))

        self.day_night.render_darkness(screen, light_sources)
        self.hud.render(screen, self.player, self.day_night.day_number, self.day_night.get_phase_name())
