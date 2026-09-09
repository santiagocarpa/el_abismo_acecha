"""
scenes/tutorial_scene.py - Escena de Tutorial y Ayuda del Juego
"""

import pygame
from config import (SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_BLACK, COLOR_TEXT_GOLD, 
                    COLOR_TEXT_WHITE, COLOR_DARK_GREEN, COLOR_UI_BG)
from scenes.base_scene import BaseScene
from ui.button import Button

class TutorialScene(BaseScene):
    def __init__(self, scene_manager):
        super().__init__(scene_manager)
        self.title_font = pygame.font.SysFont("georgia", 44, bold=True)
        self.header_font = pygame.font.SysFont("arial", 24, bold=True)
        self.text_font = pygame.font.SysFont("arial", 19)

        self.current_page = 0
        self.pages = [
            {
                "titulo": "1. OBJETIVO DEL JUEGO",
                "lineas": [
                    "• Despiertas sin recuerdos en un bosque oscuro e indocumentado.",
                    "• Tu único objetivo es sobrevivir dia a dia recolectando recursos,",
                    "  construyendo defensas y resistiendo la negrura de la noche.",
                    "",
                    "• Explora el mapa de día para talar árboles, picar piedras",
                    "  y encontrar notas escondidas sobre el origen del abismo."
                ]
            },
            {
                "titulo": "2. CONTROLES Y MOVIMIENTO",
                "lineas": [
                    "• W, A, S, D / Flechas: Mover a tu personaje en 8 direcciones.",
                    "• SHIFT IZQUIERDO: Correr / Sprint (consume barra de Energía).",
                    "• TECLA F: Interactuar / Talar árboles y picar rocas cercanas.",
                    "• TECLA C: Construir una Fogata de campo (requiere estar cerca).",
                    "• TECLA ESC: Abrir Menú de Pausa."
                ]
            },
            {
                "titulo": "3. EL CICLO DÍA / NOCHE Y LA LUZ",
                "lineas": [
                    "• DÍA (Exploración): Reúne materiales de forma segura.",
                    "• ATARDECER (Preparación): Prepara tus armas y fogatas.",
                    "• NOCHE (Supervivencia): Las sombras oscuras emergen y te perseguirán.",
                    "",
                    "• CONSEJO VITAL: Las sombras temen a la luz. ¡Mantente cerca",
                    "  de la luz de las fogatas para no caer ante la oscuridad!"
                ]
            }
        ]

        btn_w, btn_h = 200, 48
        self.btn_next = Button(SCREEN_WIDTH - 240, SCREEN_HEIGHT - 90, btn_w, btn_h, 
                               "SIGUIENTE >", self.on_next)
        self.btn_prev = Button(40, SCREEN_HEIGHT - 90, btn_w, btn_h, 
                               "< ANTERIOR", self.on_prev)
        self.btn_close = Button((SCREEN_WIDTH - btn_w) // 2, SCREEN_HEIGHT - 90, btn_w, btn_h, 
                                "ENTENDIDO", self.on_close)

    def on_next(self):
        if self.current_page < len(self.pages) - 1:
            self.current_page += 1

    def on_prev(self):
        if self.current_page > 0:
            self.current_page -= 1

    def on_close(self):
        if len(self.scene_manager.scene_stack) > 0:
            self.scene_manager.pop_scene()
        else:
            self.scene_manager.change_scene("menu")

    def handle_events(self, events):
        for event in events:
            if self.current_page < len(self.pages) - 1:
                self.btn_next.handle_event(event)
            if self.current_page > 0:
                self.btn_prev.handle_event(event)
            
            self.btn_close.handle_event(event)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.on_close()

    def update(self, dt: float):
        if self.current_page < len(self.pages) - 1:
            self.btn_next.update(dt)
        if self.current_page > 0:
            self.btn_prev.update(dt)
        self.btn_close.update(dt)

    def render(self, screen: pygame.Surface):
        # Superficie de Fondo
        screen.fill(COLOR_BLACK)

        # Marco del Tutorial
        margin_x = 80
        margin_y = 60
        box_rect = pygame.Rect(margin_x, margin_y, SCREEN_WIDTH - margin_x * 2, SCREEN_HEIGHT - margin_y * 2)
        
        box_surface = pygame.Surface((box_rect.width, box_rect.height), pygame.SRCALPHA)
        box_surface.fill(COLOR_UI_BG)
        screen.blit(box_surface, box_rect.topleft)
        pygame.draw.rect(screen, COLOR_TEXT_GOLD, box_rect, width=2, border_radius=10)

        # Título Principal
        main_title = self.title_font.render("GUÍA DE SUPERVIVENCIA", True, COLOR_TEXT_GOLD)
        screen.blit(main_title, main_title.get_rect(center=(SCREEN_WIDTH // 2, 105)))

        # Datos de la Página Actual
        page_data = self.pages[self.current_page]

        # Encabezado de sección
        header = self.header_font.render(page_data["titulo"], True, COLOR_TEXT_GOLD)
        screen.blit(header, (margin_x + 50, 165))

        # Líneas de texto
        start_text_y = 220
        for i, line in enumerate(page_data["lineas"]):
            color = COLOR_TEXT_GOLD if line.startswith("• CONSEJO") else COLOR_TEXT_WHITE
            text_surf = self.text_font.render(line, True, color)
            screen.blit(text_surf, (margin_x + 50, start_text_y + i * 32))

        # Indicador de Paginación
        page_indicator = self.text_font.render(f"Página {self.current_page + 1} / {len(self.pages)}", True, (160, 180, 170))
        screen.blit(page_indicator, page_indicator.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 120)))

        # Renderizar Botones
        if self.current_page < len(self.pages) - 1:
            self.btn_next.render(screen)
        if self.current_page > 0:
            self.btn_prev.render(screen)
        self.btn_close.render(screen)
