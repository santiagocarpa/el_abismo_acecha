"""
scenes/game_over_scene.py - Pantalla de Derrota / Muerte del Jugador
"""

import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_HEALTH_RED, COLOR_TEXT_WHITE
from scenes.base_scene import BaseScene
from ui.button import Button

class GameOverScene(BaseScene):
    def __init__(self, scene_manager):
        super().__init__(scene_manager)
        self.font = pygame.font.SysFont("georgia", 64, bold=True)
        self.sub_font = pygame.font.SysFont("arial", 24)

        btn_w, btn_h = 280, 55
        self.btn_retry = Button((SCREEN_WIDTH - btn_w) // 2, 420, btn_w, btn_h, 
                                "MENÚ PRINCIPAL", self.on_menu)

    def on_menu(self):
        self.scene_manager.change_scene("menu")

    def handle_events(self, events):
        for event in events:
            self.btn_retry.handle_event(event)

    def update(self, dt: float):
        self.btn_retry.update(dt)

    def render(self, screen: pygame.Surface):
        screen.fill((15, 5, 5))

        title = self.font.render("HAS CAÍDO EN LA OSCURIDAD", True, COLOR_HEALTH_RED)
        t_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 220))
        screen.blit(title, t_rect)

        sub = self.sub_font.render("El abismo reclamó tu alma durante la noche...", True, COLOR_TEXT_WHITE)
        s_rect = sub.get_rect(center=(SCREEN_WIDTH // 2, 300))
        screen.blit(sub, s_rect)

        self.btn_retry.render(screen)
