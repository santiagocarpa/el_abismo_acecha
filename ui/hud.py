"""
ui/hud.py - Interfaz en pantalla (HUD) del Jugador (Salud, Stamina, Reloj y Accesos)
"""

import pygame
from config import (SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_HEALTH_RED, 
                    COLOR_STAMINA_GREEN, COLOR_TEXT_WHITE, COLOR_TEXT_GOLD, COLOR_UI_BG)

class HUD:
    def __init__(self):
        self.font = pygame.font.SysFont("arial", 18, bold=True)
        self.large_font = pygame.font.SysFont("arial", 22, bold=True)

    def render(self, screen: pygame.Surface, player, day_number: int, day_time_text: str):
        # 1. Panel de Salud y Stamina (Esquina Superior Izquierda)
        panel_rect = pygame.Rect(20, 20, 260, 85)
        panel_surface = pygame.Surface((panel_rect.width, panel_rect.height), pygame.SRCALPHA)
        panel_surface.fill(COLOR_UI_BG)
        screen.blit(panel_surface, panel_rect.topleft)
        pygame.draw.rect(screen, COLOR_TEXT_GOLD, panel_rect, width=2, border_radius=4)

        # Barra de Salud (HP)
        hp_pct = max(0.0, min(1.0, player.salud / player.salud_max))
        pygame.draw.rect(screen, (50, 20, 20), (35, 32, 210, 18), border_radius=3)
        if hp_pct > 0:
            pygame.draw.rect(screen, COLOR_HEALTH_RED, (35, 32, int(210 * hp_pct), 18), border_radius=3)
        hp_text = self.font.render(f"HP: {player.salud}/{player.salud_max}", True, COLOR_TEXT_WHITE)
        screen.blit(hp_text, (40, 32))

        # Barra de Stamina
        stamina_pct = max(0.0, min(1.0, player.stamina / player.stamina_max))
        pygame.draw.rect(screen, (20, 50, 20), (35, 62, 210, 16), border_radius=3)
        if stamina_pct > 0:
            pygame.draw.rect(screen, COLOR_STAMINA_GREEN, (35, 62, int(210 * stamina_pct), 16), border_radius=3)
        stamina_text = self.font.render(f"Energía: {int(player.stamina)}%", True, COLOR_TEXT_WHITE)
        screen.blit(stamina_text, (40, 62))

        # 2. Panel del Reloj y Día (Esquina Superior Derecha)
        clock_rect = pygame.Rect(SCREEN_WIDTH - 220, 20, 200, 65)
        clock_surface = pygame.Surface((clock_rect.width, clock_rect.height), pygame.SRCALPHA)
        clock_surface.fill(COLOR_UI_BG)
        screen.blit(clock_surface, clock_rect.topleft)
        pygame.draw.rect(screen, COLOR_TEXT_GOLD, clock_rect, width=2, border_radius=4)

        dia_txt = self.large_font.render(f"Día {day_number}", True, COLOR_TEXT_GOLD)
        fase_txt = self.font.render(f"Estado: {day_time_text}", True, COLOR_TEXT_WHITE)
        screen.blit(dia_txt, (SCREEN_WIDTH - 205, 26))
        screen.blit(fase_txt, (SCREEN_WIDTH - 205, 54))

        # 3. Hotbar Inferior de Acceso Rápido
        hotbar_width = 8 * 52 + 10
        hotbar_rect = pygame.Rect((SCREEN_WIDTH - hotbar_width) // 2, SCREEN_HEIGHT - 70, hotbar_width, 58)
        hotbar_bg = pygame.Surface((hotbar_rect.width, hotbar_rect.height), pygame.SRCALPHA)
        hotbar_bg.fill(COLOR_UI_BG)
        screen.blit(hotbar_bg, hotbar_rect.topleft)
        pygame.draw.rect(screen, COLOR_TEXT_GOLD, hotbar_rect, width=2, border_radius=6)

        for i in range(8):
            slot_x = hotbar_rect.x + 8 + i * 52
            slot_rect = pygame.Rect(slot_x, hotbar_rect.y + 7, 44, 44)
            pygame.draw.rect(screen, (35, 45, 40), slot_rect, border_radius=4)
            pygame.draw.rect(screen, (80, 100, 90), slot_rect, width=1, border_radius=4)
            idx_txt = self.font.render(str(i + 1), True, (150, 160, 150))
            screen.blit(idx_txt, (slot_x + 4, slot_rect.y + 2))
