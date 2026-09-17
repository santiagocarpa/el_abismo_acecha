"""
ui/crafting_ui.py - Interfaz Modal de Inventario y Crafteo en Pantalla
"""

import pygame
from config import (SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_UI_BG, 
                    COLOR_TEXT_GOLD, COLOR_TEXT_WHITE, COLOR_HEALTH_RED, COLOR_STAMINA_GREEN)
from systems.inventory import ITEM_DEFINITIONS
from systems.crafting import CraftingSystem
from ui.button import Button

class CraftingUI:
    def __init__(self, inventory):
        self.inventory = inventory
        self.is_open = False
        self.recipes = CraftingSystem.get_recipes()
        self.selected_recipe_idx = 0
        self.feedback_msg = ""
        self.feedback_timer = 0.0

        # Fuentes
        self.title_font = pygame.font.SysFont("georgia", 28, bold=True)
        self.sub_font = pygame.font.SysFont("arial", 20, bold=True)
        self.small_font = pygame.font.SysFont("arial", 15)
        self.count_font = pygame.font.SysFont("arial", 14, bold=True)

        # Dimensiones del Panel Modal
        self.width = 960
        self.height = 560
        self.rect = pygame.Rect((SCREEN_WIDTH - self.width) // 2, (SCREEN_HEIGHT - self.height) // 2, self.width, self.height)

        # Botón de Fabricar
        self.btn_craft = Button(self.rect.x + 600, self.rect.y + 475, 280, 50, 
                                "FABRICAR (ESPACIO)", self.on_craft_clicked, font_size=20)
        self.btn_close = Button(self.rect.right - 45, self.rect.y + 15, 30, 30, 
                                "X", self.toggle, font_size=18, bg_color=(120, 40, 40))

    def toggle(self):
        self.is_open = not self.is_open
        self.feedback_msg = ""

    def on_craft_clicked(self):
        if not self.is_open:
            return

        recipe = self.recipes[self.selected_recipe_idx]
        success = CraftingSystem.craft(recipe, self.inventory)
        if success:
            self.feedback_msg = f"¡Fabricado con éxito: 1x {recipe['nombre']}!"
            self.feedback_timer = 2.5
        else:
            self.feedback_msg = "¡Materiales insuficientes!"
            self.feedback_timer = 2.5

    def handle_event(self, event):
        if not self.is_open:
            return

        self.btn_craft.handle_event(event)
        self.btn_close.handle_event(event)

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_c, pygame.K_e, pygame.K_ESCAPE):
                self.toggle()
            elif event.key == pygame.K_UP:
                self.selected_recipe_idx = (self.selected_recipe_idx - 1) % len(self.recipes)
            elif event.key == pygame.K_DOWN:
                self.selected_recipe_idx = (self.selected_recipe_idx + 1) % len(self.recipes)
            elif event.key in (pygame.K_SPACE, pygame.K_RETURN):
                self.on_craft_clicked()

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Detectar clic en la lista de recetas
            list_top = self.rect.y + 100
            for idx, r in enumerate(self.recipes):
                r_rect = pygame.Rect(self.rect.x + 520, list_top + idx * 58, 380, 52)
                if r_rect.collidepoint(event.pos):
                    self.selected_recipe_idx = idx

    def update(self, dt: float):
        if not self.is_open:
            return

        self.btn_craft.update(dt)
        self.btn_close.update(dt)

        if self.feedback_timer > 0:
            self.feedback_timer -= dt
            if self.feedback_timer <= 0:
                self.feedback_msg = ""

    def render(self, screen: pygame.Surface):
        if not self.is_open:
            return

        # Fondo semitransparente oscuro
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((5, 10, 8, 200))
        screen.blit(overlay, (0, 0))

        # Panel Modal Principal
        panel_bg = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        panel_bg.fill(COLOR_UI_BG)
        screen.blit(panel_bg, self.rect.topleft)
        pygame.draw.rect(screen, COLOR_TEXT_GOLD, self.rect, width=2, border_radius=10)

        # Título
        title_surf = self.title_font.render("INVENTARIO Y CRAFTEO", True, COLOR_TEXT_GOLD)
        screen.blit(title_surf, (self.rect.x + 30, self.rect.y + 20))

        # -------------------------------------------------------------
        # 1. PANEL IZQUIERDO: INVENTARIO (Grilla 4x4)
        # -------------------------------------------------------------
        inv_title = self.sub_font.render("TUS RECURSOS", True, COLOR_TEXT_WHITE)
        screen.blit(inv_title, (self.rect.x + 30, self.rect.y + 70))

        grid_start_x = self.rect.x + 30
        grid_start_y = self.rect.y + 105
        slot_size = 95
        gap = 12

        for idx in range(16):
            row = idx // 4
            col = idx % 4
            sx = grid_start_x + col * (slot_size + gap)
            sy = grid_start_y + row * (slot_size + gap)
            s_rect = pygame.Rect(sx, sy, slot_size, slot_size)

            pygame.draw.rect(screen, (30, 42, 36), s_rect, border_radius=6)
            pygame.draw.rect(screen, (70, 95, 80), s_rect, width=1, border_radius=6)

            slot = self.inventory.slots[idx] if idx < len(self.inventory.slots) else None
            if slot:
                item_info = ITEM_DEFINITIONS.get(slot["item_id"], {})
                color = item_info.get("color", (200, 200, 200))

                # Icono de color del objeto
                icon_rect = pygame.Rect(sx + 24, sy + 14, 46, 42)
                pygame.draw.rect(screen, color, icon_rect, border_radius=4)
                pygame.draw.rect(screen, (255, 255, 255), icon_rect, width=1, border_radius=4)

                # Nombre del ítem
                name_txt = self.small_font.render(item_info.get("nombre", slot["item_id"]), True, COLOR_TEXT_WHITE)
                screen.blit(name_txt, (sx + 6, sy + 58))

                # Badge de Cantidad
                qty_txt = self.count_font.render(f"x{slot['cantidad']}", True, COLOR_TEXT_GOLD)
                screen.blit(qty_txt, (sx + slot_size - 32, sy + slot_size - 18))

        # -------------------------------------------------------------
        # 2. PANEL DERECHO: RECETAS DE FABRICACIÓN
        # -------------------------------------------------------------
        rec_title = self.sub_font.render("RECETAS DE CRAFTEO", True, COLOR_TEXT_WHITE)
        screen.blit(rec_title, (self.rect.x + 520, self.rect.y + 70))

        list_top = self.rect.y + 105
        for idx, r in enumerate(self.recipes):
            r_rect = pygame.Rect(self.rect.x + 520, list_top + idx * 58, 410, 52)
            is_selected = (idx == self.selected_recipe_idx)
            can_craft = CraftingSystem.can_craft(r, self.inventory)

            bg_col = (45, 65, 52) if is_selected else (25, 36, 30)
            border_col = COLOR_TEXT_GOLD if is_selected else (60, 85, 70)

            pygame.draw.rect(screen, bg_col, r_rect, border_radius=6)
            pygame.draw.rect(screen, border_col, r_rect, width=2 if is_selected else 1, border_radius=6)

            # Nombre de la receta
            r_name = self.sub_font.render(r["nombre"], True, COLOR_TEXT_GOLD if is_selected else COLOR_TEXT_WHITE)
            screen.blit(r_name, (r_rect.x + 12, r_rect.y + 6))

            # Ingredientes requeridos e indicador visual de disponibilidad
            req_str = []
            for item_req, qty in r["ingredientes"].items():
                item_name = ITEM_DEFINITIONS.get(item_req, {}).get("nombre", item_req)
                have_qty = self.inventory.get_item_count(item_req)
                req_str.append(f"{item_name}: {have_qty}/{qty}")

            req_txt = self.small_font.render(" | ".join(req_str), True, COLOR_STAMINA_GREEN if can_craft else COLOR_HEALTH_RED)
            screen.blit(req_txt, (r_rect.x + 12, r_rect.y + 30))

        # Descripción y Botón
        sel_rec = self.recipes[self.selected_recipe_idx]
        desc_txt = self.small_font.render(sel_rec["descripcion"], True, (200, 210, 200))
        screen.blit(desc_txt, (self.rect.x + 520, self.rect.y + 450))

        # Mensaje de Feedback
        if self.feedback_msg:
            fb_color = COLOR_STAMINA_GREEN if "éxito" in self.feedback_msg else COLOR_HEALTH_RED
            fb_surf = self.sub_font.render(self.feedback_msg, True, fb_color)
            screen.blit(fb_surf, (self.rect.x + 30, self.rect.y + self.height - 35))

        self.btn_craft.render(screen)
        self.btn_close.render(screen)
