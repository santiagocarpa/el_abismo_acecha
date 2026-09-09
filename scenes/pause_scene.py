"""
scenes/pause_scene.py - Menú de Pausa en Overlay
"""

import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_UI_BG, COLOR_TEXT_GOLD
from scenes.base_scene import BaseScene
from ui.button import Button

class PauseScene(BaseScene):
    def __init__(self, scene_manager):
        super().__init__(scene_manager)
        self.font = pygame.font.SysFont("georgia", 48, bold=True)

        btn_w, btn_h = 260, 50
        start_y = 280
        spacing = 65

        self.buttons = [
            Button((SCREEN_WIDTH - btn_w) // 2, start_y, btn_w, btn_h, 
                   "REANUDAR", self.on_resume),
            Button((SCREEN_WIDTH - btn_w) // 2, start_y + spacing, btn_w, btn_h, 
                   "MENÚ PRINCIPAL", self.on_main_menu)
        ]

    def on_resume(self):
        self.scene_manager.pop_scene()

    def on_main_menu(self):
        self.scene_manager.pop_scene()
        self.scene_manager.change_scene("menu")

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.on_resume()
            for btn in self.buttons:
                btn.handle_event(event)

    def update(self, dt: float):
        for btn in self.buttons:
            btn.update(dt)

    def render(self, screen: pygame.Surface):
        # Superficie semitransparente de fondo
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((10, 15, 12, 180))
        screen.blit(overlay, (0, 0))

        # Cuadro de Pausa
        box_rect = pygame.Rect((SCREEN_WIDTH - 360) // 2, 180, 360, 320)
        pygame.draw.rect(screen, COLOR_UI_BG, box_rect, border_radius=8)
        pygame.draw.rect(screen, COLOR_TEXT_GOLD, box_rect, width=2, border_radius=8)

        # Título
        title_surf = self.font.render("PAUSA", True, COLOR_TEXT_GOLD)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 230))
        screen.blit(title_surf, title_rect)

        # Botones
        for btn in self.buttons:
            btn.render(screen)
