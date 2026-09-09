"""
systems/day_night.py - Sistema de Reloj y Iluminación Ambiental Día / Atardecer / Noche
"""

import pygame
import math
from config import SCREEN_WIDTH, SCREEN_HEIGHT

class DayNightSystem:
    def __init__(self, cycle_duration: float = 120.0):
        self.cycle_duration = cycle_duration  # Segundos por ciclo completo de día/noche
        self.time = 0.0  # Tiempo acumulado del día
        self.day_number = 1
        self.ambient_darkness = 0.0  # Alpha de 0 (Día) a 210 (Noche oscura)

    def update(self, dt: float):
        self.time += dt
        if self.time >= self.cycle_duration:
            self.time -= self.cycle_duration
            self.day_number += 1

        # Proporción del día (0.0 a 1.0)
        progress = self.time / self.cycle_duration

        # 0.0 -> 0.5: Día (Luz normal)
        # 0.5 -> 0.7: Atardecer (Transición)
        # 0.7 -> 0.95: Noche (Oscuridad máxima)
        # 0.95 -> 1.0: Amanecer
        if progress < 0.5:
            self.ambient_darkness = 0.0
        elif progress < 0.7:
            t = (progress - 0.5) / 0.2
            self.ambient_darkness = t * 210.0
        elif progress < 0.95:
            self.ambient_darkness = 210.0
        else:
            t = (progress - 0.95) / 0.05
            self.ambient_darkness = (1.0 - t) * 210.0

    def get_phase_name(self) -> str:
        progress = self.time / self.cycle_duration
        if progress < 0.5:
            return "Día (Exploración)"
        elif progress < 0.7:
            return "Atardecer (Preparación)"
        elif progress < 0.95:
            return "Noche (Peligro)"
        else:
            return "Amanecer"

    def render_darkness(self, screen: pygame.Surface, light_sources=None):
        """Dibuja la capa de penumbra y aplica luces focales (fogatas, antorchas)."""
        if self.ambient_darkness <= 5.0:
            return

        dark_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        dark_surface.fill((10, 15, 25, int(self.ambient_darkness)))

        # Si hay fuentes de luz (Fogatas, Antorchas), se recortan círculos transparentes en la máscara
        if light_sources:
            for light_pos, radius in light_sources:
                # Recortar luz con blending subtractivo
                light_mask = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                for r in range(radius, 0, -4):
                    alpha = int(self.ambient_darkness * (r / radius))
                    pygame.draw.circle(light_mask, (0, 0, 0, alpha), (radius, radius), r)
                
                dark_surface.blit(light_mask, (light_pos[0] - radius, light_pos[1] - radius), special_flags=pygame.BLEND_RGBA_SUB)

        screen.blit(dark_surface, (0, 0))
