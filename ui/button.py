"""
ui/button.py - Componente de Botón Interactivo para la UI del Juego
"""

import pygame
from config import COLOR_TEXT_WHITE, COLOR_TEXT_GOLD, COLOR_DARK_GREEN, COLOR_FOG_GREEN

class Button:
    def __init__(self, x: int, y: int, width: int, height: int, text: str, callback=None, 
                 font_size: int = 28, bg_color=COLOR_DARK_GREEN, hover_color=COLOR_FOG_GREEN):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.font = pygame.font.SysFont("arial", font_size, bold=True)
        self.is_hovered = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered and self.callback:
                self.callback()

    def update(self, dt: float):
        # Actualiza el estado de hover en caso de movimiento de mouse continuo
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def render(self, screen: pygame.Surface):
        # Color de fondo según hover
        current_bg = self.hover_color if self.is_hovered else self.bg_color
        border_color = COLOR_TEXT_GOLD if self.is_hovered else COLOR_TEXT_WHITE
        text_color = COLOR_TEXT_GOLD if self.is_hovered else COLOR_TEXT_WHITE

        # Dibujar rectángulo de fondo y borde
        pygame.draw.rect(screen, current_bg, self.rect, border_radius=6)
        pygame.draw.rect(screen, border_color, self.rect, width=2, border_radius=6)

        # Renderizar texto centrado
        text_surface = self.font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
