"""
ui/hud.py - Interfaz en pantalla (HUD) del Jugador con Hotbar e Indicador de Agotamiento
"""

import pygame
from config import (SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_HEALTH_RED, 
                    COLOR_STAMINA_GREEN, COLOR_TEXT_WHITE, COLOR_TEXT_GOLD, COLOR_UI_BG)
from systems.inventory import ITEM_DEFINITIONS

class HUD:
    def __init__(self):
        self.font = pygame.font.SysFont("arial", 17, bold=True)
        self.large_font = pygame.font.SysFont("arial", 22, bold=True)
        self.notification_msg = ""
        self.notification_timer = 0.0

    def show_notification(self, text: str, duration: float = 2.0):
        self.notification_msg = text
        self.notification_timer = duration

    def update(self, dt: float):
        if self.notification_timer > 0:
            self.notification_timer -= dt
            if self.notification_timer <= 0:
                self.notification_msg = ""

    def render(self, screen: pygame.Surface, player, day_number: int, day_time_text: str, inventory=None):
        # 1. Panel de Salud y Stamina (Esquina Superior Izquierda)
        panel_rect = pygame.Rect(20, 20, 270, 90)
        panel_surface = pygame.Surface((panel_rect.width, panel_rect.height), pygame.SRCALPHA)
        panel_surface.fill(COLOR_UI_BG)
        screen.blit(panel_surface, panel_rect.topleft)
        pygame.draw.rect(screen, COLOR_TEXT_GOLD, panel_rect, width=2, border_radius=4)

        # Barra de Salud (HP)
        hp_pct = max(0.0, min(1.0, player.salud / player.salud_max))
        pygame.draw.rect(screen, (50, 20, 20), (35, 32, 220, 18), border_radius=3)
        if hp_pct > 0:
            pygame.draw.rect(screen, COLOR_HEALTH_RED, (35, 32, int(220 * hp_pct), 18), border_radius=3)
        hp_text = self.font.render(f"HP: {int(player.salud)}/{player.salud_max}", True, COLOR_TEXT_WHITE)
        screen.blit(hp_text, (40, 32))

        # Barra de Stamina (Con Estado de Agotamiento)
        stamina_pct = max(0.0, min(1.0, player.stamina / player.stamina_max))
        pygame.draw.rect(screen, (20, 50, 20), (35, 62, 220, 16), border_radius=3)
        
        if player.is_exhausted:
            stamina_bar_color = (200, 80, 40)
            stamina_label = "¡AGOTADO!"
        else:
            stamina_bar_color = COLOR_STAMINA_GREEN
            stamina_label = f"Energía: {int(player.stamina)}%"

        if stamina_pct > 0:
            pygame.draw.rect(screen, stamina_bar_color, (35, 62, int(220 * stamina_pct), 16), border_radius=3)
        
        stamina_text = self.font.render(stamina_label, True, COLOR_TEXT_WHITE)
        screen.blit(stamina_text, (40, 62))

        # 2. Panel del Reloj y Día (Esquina Superior Derecha)
        clock_rect = pygame.Rect(SCREEN_WIDTH - 240, 20, 220, 75)
        clock_surface = pygame.Surface((clock_rect.width, clock_rect.height), pygame.SRCALPHA)
        clock_surface.fill(COLOR_UI_BG)
        screen.blit(clock_surface, clock_rect.topleft)
        pygame.draw.rect(screen, COLOR_TEXT_GOLD, clock_rect, width=2, border_radius=4)

        dia_txt = self.large_font.render(f"Día {day_number}", True, COLOR_TEXT_GOLD)
        fase_txt = self.font.render(f"{day_time_text}", True, COLOR_TEXT_WHITE)
        screen.blit(dia_txt, (SCREEN_WIDTH - 225, 26))
        screen.blit(fase_txt, (SCREEN_WIDTH - 225, 54))

        # 3. Hotbar Inferior de Acceso Rápido con Ítems del Inventario
        hotbar_count = 8
        slot_w = 54
        hotbar_width = hotbar_count * slot_w + 12
        hotbar_rect = pygame.Rect((SCREEN_WIDTH - hotbar_width) // 2, SCREEN_HEIGHT - 75, hotbar_width, 62)
        hotbar_bg = pygame.Surface((hotbar_rect.width, hotbar_rect.height), pygame.SRCALPHA)
        hotbar_bg.fill(COLOR_UI_BG)
        screen.blit(hotbar_bg, hotbar_rect.topleft)
        pygame.draw.rect(screen, COLOR_TEXT_GOLD, hotbar_rect, width=2, border_radius=6)

        for i in range(hotbar_count):
            slot_x = hotbar_rect.x + 8 + i * slot_w
            slot_rect = pygame.Rect(slot_x, hotbar_rect.y + 7, 46, 46)
            pygame.draw.rect(screen, (35, 45, 40), slot_rect, border_radius=4)
            pygame.draw.rect(screen, (80, 100, 90), slot_rect, width=1, border_radius=4)

            # Dibujar contenido si existe en inventario
            if inventory and i < len(inventory.slots) and inventory.slots[i]:
                slot_data = inventory.slots[i]
                item_info = ITEM_DEFINITIONS.get(slot_data["item_id"], {})
                icon_rect = pygame.Rect(slot_x + 8, slot_rect.y + 8, 30, 24)
                pygame.draw.rect(screen, item_info.get("color", (200, 200, 200)), icon_rect, border_radius=3)
                
                # Cantidad
                qty_surf = self.font.render(f"x{slot_data['cantidad']}", True, COLOR_TEXT_GOLD)
                screen.blit(qty_surf, (slot_x + 16, slot_rect.y + 26))

            idx_txt = self.font.render(str(i + 1), True, (160, 170, 160))
            screen.blit(idx_txt, (slot_x + 3, slot_rect.y + 1))

        # 4. Indicador de Tecla para Abrir Menú
        hint_txt = self.font.render("[Presiona 'C' o 'E' para Abrir Inventario / Crafteo]", True, COLOR_TEXT_GOLD)
        screen.blit(hint_txt, hint_txt.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 95)))

        # 5. Notificaciones Flotantes de Recolección
        if self.notification_msg:
            notif_surf = self.large_font.render(self.notification_msg, True, COLOR_TEXT_GOLD)
            n_bg = pygame.Surface((notif_surf.get_width() + 20, 36), pygame.SRCALPHA)
            n_bg.fill((10, 20, 15, 220))
            n_rect = n_bg.get_rect(center=(SCREEN_WIDTH // 2, 130))
            screen.blit(n_bg, n_rect)
            screen.blit(notif_surf, notif_surf.get_rect(center=n_rect.center))
