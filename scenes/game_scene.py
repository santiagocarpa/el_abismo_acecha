"""
scenes/game_scene.py - Escena Principal de Juego con Inventario, Crafteo, Combate y Muerte Limpia
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
from systems.inventory import Inventory
from ui.hud import HUD
from ui.crafting_ui import CraftingUI
from core.database import DatabaseManager

class GameScene(BaseScene):
    def __init__(self, scene_manager):
        super().__init__(scene_manager)
        self.db = DatabaseManager()
        self.hud = HUD()

        self.inventory = Inventory(capacity=16)
        self.crafting_ui = CraftingUI(self.inventory)

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

        self.player.inventory = self.inventory

        # Dar materiales iniciales de bienvenida (3 Madera, 1 Piedra)
        self.inventory.add_item("madera", 3)
        self.inventory.add_item("piedra", 1)

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
        # Árboles (Madera)
        for _ in range(80):
            rx = random.randint(100, WORLD_WIDTH - 100)
            ry = random.randint(100, WORLD_HEIGHT - 100)
            self.resource_nodes.append(ResourceNode(rx, ry, "arbol"))

        # Rocas (Piedra)
        for _ in range(35):
            rx = random.randint(100, WORLD_WIDTH - 100)
            ry = random.randint(100, WORLD_HEIGHT - 100)
            self.resource_nodes.append(ResourceNode(rx, ry, "roca"))

        # Vetas de Hierro
        for _ in range(20):
            rx = random.randint(100, WORLD_WIDTH - 100)
            ry = random.randint(100, WORLD_HEIGHT - 100)
            self.resource_nodes.append(ResourceNode(rx, ry, "hierro"))

        # Fogata inicial
        self.structures.append(Structure(WORLD_WIDTH // 2 + 60, WORLD_HEIGHT // 2 + 60, "fogata"))

    def handle_events(self, events):
        for event in events:
            # Si el menú de crafteo está abierto, redirigir eventos allí
            if self.crafting_ui.is_open:
                self.crafting_ui.handle_event(event)
                continue

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.scene_manager.push_scene("pause")
                elif event.key in (pygame.K_c, pygame.K_e):
                    self.crafting_ui.toggle()
                elif event.key == pygame.K_f:
                    self._interact_or_gather()
                elif event.key == pygame.K_SPACE:
                    self._player_attack()
                elif event.key == pygame.K_b:
                    self._place_structure_from_inventory()

    def _interact_or_gather(self):
        """Recolecta recursos cercanos y los almacena en el inventario."""
        for node in list(self.resource_nodes):
            dist = (self.player.pos - node.pos).length()
            if dist < 55.0:
                destruido = node.recibir_dano(1)
                
                # Tipo de recurso otorgado
                if node.resource_type == "arbol":
                    res_id, cantidad = "madera", 2
                elif node.resource_type == "roca":
                    res_id, cantidad = "piedra", 2
                else:
                    res_id, cantidad = "hierro", 1

                self.inventory.add_item(res_id, cantidad)
                self.hud.show_notification(f"+{cantidad} {res_id.capitalize()} recolectada")

                if destruido:
                    self.resource_nodes.remove(node)
                break

    def _player_attack(self):
        """Ataque del jugador contra sombras enemigas cercanas."""
        tiene_espada = self.inventory.get_item_count("espada") > 0
        dano_ataque = 35 if tiene_espada else 12

        for enemy in list(self.enemies):
            dist = (self.player.pos - enemy.pos).length()
            if dist < 65.0:
                enemy.salud -= dano_ataque
                self.hud.show_notification(f"¡Ataque a Sombra! -{dano_ataque} HP")
                if enemy.salud <= 0:
                    self.enemies.remove(enemy)
                break

    def _place_structure_from_inventory(self):
        """Coloca una estructura (Fogata o Muro) si existe en el inventario."""
        if self.inventory.get_item_count("fogata") > 0:
            self.inventory.remove_item("fogata", 1)
            self.structures.append(Structure(self.player.x + 35, self.player.y, "fogata"))
            self.hud.show_notification("¡Fogata de Campo colocada!")
        elif self.inventory.get_item_count("muro_madera") > 0:
            self.inventory.remove_item("muro_madera", 1)
            self.structures.append(Structure(self.player.x + 35, self.player.y, "muro_madera"))
            self.hud.show_notification("¡Muro de Madera colocado!")
        else:
            self.hud.show_notification("Fabrica una Fogata o Muro primero (Tecla C)")

    def update(self, dt: float):
        # 1. Si el jugador está muerto, forzar inmediatamente la pantalla de Game Over
        if self.player.is_dead or self.player.salud <= 0:
            self.scene_manager.change_scene("game_over", with_fade=False)
            return

        # 2. Si el menú modal de crafteo está abierto, pausar el mundo
        if self.crafting_ui.is_open:
            self.crafting_ui.update(dt)
            return

        # 3. Actualizar Reloj y HUD
        self.day_night.update(dt)
        self.hud.update(dt)

        # 4. Actualizar Jugador y Entidades
        self.player.actualizar(dt, obstaculos=self.structures)

        # Spawning de Enemigos durante la Noche
        if self.day_night.get_phase_name().startswith("Noche") and len(self.enemies) < 6:
            if random.random() < 0.025:
                spawn_x = self.player.x + random.choice([-450, 450])
                spawn_y = self.player.y + random.choice([-350, 350])
                self.enemies.append(Enemy(spawn_x, spawn_y))

        # Actualizar Enemigos según máquina de estados (PATRULLA, PERSECUCION, ATAQUE)
        for enemy in list(self.enemies):
            enemy.set_target_player(self.player)
            enemy.actualizar(dt, obstaculos=self.structures)

        for node in self.resource_nodes:
            node.actualizar(dt)

        for struct in self.structures:
            struct.actualizar(dt)

        # Cámara centrada en el jugador
        self.camera_offset.x = self.player.x - SCREEN_WIDTH // 2
        self.camera_offset.y = self.player.y - SCREEN_HEIGHT // 2

    def render(self, screen: pygame.Surface):
        # Terreno y Entidades
        screen.blit(self.terrain_surface, (-self.camera_offset.x, -self.camera_offset.y))

        for node in self.resource_nodes:
            node.dibujar(screen, self.camera_offset)

        for struct in self.structures:
            struct.dibujar(screen, self.camera_offset)

        for enemy in self.enemies:
            enemy.dibujar(screen, self.camera_offset)

        self.player.dibujar(screen, self.camera_offset)

        # Fuentes de Luz (Fogatas y Antorchas)
        light_sources = []
        for struct in self.structures:
            if struct.light_radius > 0:
                screen_pos = (int(struct.x - self.camera_offset.x), int(struct.y - self.camera_offset.y))
                light_sources.append((screen_pos, struct.light_radius))

        # Luz del jugador (Aumenta si porta Antorcha)
        has_torch = self.inventory.get_item_count("antorcha") > 0
        p_light_radius = 160 if has_torch else 90
        player_screen_pos = (int(self.player.x - self.camera_offset.x), int(self.player.y - self.camera_offset.y))
        light_sources.append((player_screen_pos, p_light_radius))

        # Penumbra Ambiental Día/Noche
        self.day_night.render_darkness(screen, light_sources)

        # Renderizar HUD en pantalla fija
        self.hud.render(screen, self.player, self.day_night.day_number, self.day_night.get_phase_name(), inventory=self.inventory)

        # Renderizar Menú Modal de Crafteo
        self.crafting_ui.render(screen)
