"""
core/engine.py - Motor Principal del Juego con Escena de Tutorial
"""

import pygame
import sys
from config import SCREEN_WIDTH, SCREEN_HEIGHT, TITLE, FPS_CAP, MAX_DELTA_TIME
from core.scene_manager import SceneManager
from scenes.menu_scene import MenuScene
from scenes.game_scene import GameScene
from scenes.pause_scene import PauseScene
from scenes.game_over_scene import GameOverScene
from scenes.tutorial_scene import TutorialScene

class Engine:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption(TITLE)

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.is_running = False

        # Inicialización del Gestor de Escenas
        self.scene_manager = SceneManager(self)
        self._setup_scenes()

    def _setup_scenes(self):
        """Registra las escenas del juego en el SceneManager."""
        self.scene_manager.register_scene("menu", MenuScene(self.scene_manager))
        self.scene_manager.register_scene("game", GameScene(self.scene_manager))
        self.scene_manager.register_scene("pause", PauseScene(self.scene_manager))
        self.scene_manager.register_scene("game_over", GameOverScene(self.scene_manager))
        self.scene_manager.register_scene("tutorial", TutorialScene(self.scene_manager))

        # Iniciar en el Menú Principal
        self.scene_manager.change_scene("menu", with_fade=False)

    def run(self):
        """Ciclo Principal del Juego (Game Loop Frame-Independent)."""
        self.is_running = True

        while self.is_running:
            # 1. Cálculo del Delta Time (dt) en segundos
            delta_time_ms = self.clock.tick(FPS_CAP)
            dt = delta_time_ms / 1000.0

            # Delta Clamping para prevenir saltos de física o tunneling
            dt = min(dt, MAX_DELTA_TIME)

            # 2. Manejo de Eventos de Pygame
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.is_running = False

            self.scene_manager.handle_events(events)

            # 3. Actualización de Lógica con Delta Time
            self.scene_manager.update(dt)

            # 4. Renderizado y Flip de Buffer
            self.scene_manager.render(self.screen)
            pygame.display.flip()

        pygame.quit()
        sys.exit()
