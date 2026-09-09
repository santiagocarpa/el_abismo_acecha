"""
scenes/menu_scene.py - Escena de Menú Principal con Tutorial/Ayuda
"""

import pygame
import sys
from config import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_BLACK, COLOR_TEXT_GOLD, COLOR_TEXT_WHITE
from scenes.base_scene import BaseScene
from ui.button import Button
from core.database import DatabaseManager

class MenuScene(BaseScene):
    def __init__(self, scene_manager):
        super().__init__(scene_manager)
        self.db = DatabaseManager()

        # Título y Fuentes
        self.title_font = pygame.font.SysFont("georgia", 64, bold=True)
        self.subtitle_font = pygame.font.SysFont("arial", 22, italic=True)

        # Botones del Menú
        btn_width, btn_height = 280, 50
        start_y = 310
        spacing = 62

        self.buttons = [
            Button((SCREEN_WIDTH - btn_width) // 2, start_y, btn_width, btn_height, 
                   "NUEVA PARTIDA", self.on_new_game),
            Button((SCREEN_WIDTH - btn_width) // 2, start_y + spacing, btn_width, btn_height, 
                   "TUTORIAL / AYUDA", self.on_tutorial),
            Button((SCREEN_WIDTH - btn_width) // 2, start_y + spacing * 2, btn_width, btn_height, 
                   "CARGAR PARTIDA", self.on_load_game),
            Button((SCREEN_WIDTH - btn_width) // 2, start_y + spacing * 3, btn_width, btn_height, 
                   "SALIR", self.on_exit_game)
        ]

    def on_new_game(self):
        partida_id = self.db.crear_nueva_partida("Partida 1")
        # Abre el tutorial primero antes de empezar la partida
        self.scene_manager.push_scene("tutorial")
        self.scene_manager.change_scene("game", data={"partida_id": partida_id})

    def on_tutorial(self):
        self.scene_manager.push_scene("tutorial")

    def on_load_game(self):
        partidas = self.db.obtener_partidas()
        if partidas:
            partida_id = partidas[0]["id"]
            self.scene_manager.change_scene("game", data={"partida_id": partida_id})
        else:
            self.on_new_game()

    def on_exit_game(self):
        pygame.quit()
        sys.exit()

    def handle_events(self, events):
        for event in events:
            for btn in self.buttons:
                btn.handle_event(event)

    def update(self, dt: float):
        for btn in self.buttons:
            btn.update(dt)

    def render(self, screen: pygame.Surface):
        screen.fill(COLOR_BLACK)

        # Fondo estilizado
        pygame.draw.rect(screen, (15, 28, 20), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.draw.circle(screen, (30, 60, 45), (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), 380)

        # Título y Subtítulo
        title_surf = self.title_font.render("EL ABISMO ACECHA", True, COLOR_TEXT_GOLD)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 150))
        screen.blit(title_surf, title_rect)

        sub_surf = self.subtitle_font.render("Sobrevive a la negrura del bosque sin nombre", True, COLOR_TEXT_WHITE)
        sub_rect = sub_surf.get_rect(center=(SCREEN_WIDTH // 2, 210))
        screen.blit(sub_surf, sub_rect)

        # Renderizar Botones
        for btn in self.buttons:
            btn.render(screen)
