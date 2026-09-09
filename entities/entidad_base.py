"""
entities/entidad_base.py - Clase madre abstracta EntidadBase
Estructura arquitectónica con x, y, vx, vy, hitbox, caída libre, 
desplazamiento horizontal, actualización espacial y resolución de colisiones.
"""

from abc import ABC, abstractmethod
import pygame

class EntidadBase(ABC, pygame.sprite.Sprite):
    def __init__(self, x: float, y: float, ancho: int, alto: int, aplica_gravedad: bool = False):
        super().__init__()
        # Coordenadas continuas flotantes
        self.x = float(x)
        self.y = float(y)
        self.ancho = ancho
        self.alto = alto

        # Vectores de velocidad horizontal (vx) y vertical (vy)
        self.vx = 0.0
        self.vy = 0.0

        # Caída libre / Gravedad
        self.aplica_gravedad = aplica_gravedad
        self.gravedad = 400.0  # Píxeles por segundo al cuadrado

        # Superficie de renderizado
        self.image = pygame.Surface((ancho, alto), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(int(self.x), int(self.y)))
        
        # Hitbox para colisiones físicas
        self.hitbox = self.rect.inflate(-4, -4)

    @abstractmethod
    def actualizar_logica(self, dt: float):
        """Método abstracto para la lógica interna específica de cada entidad."""
        pass

    def aplicar_caida_libre(self, dt: float):
        """1. Caída libre: Aplica la aceleración de gravedad sobre la velocidad vertical vy."""
        if self.aplica_gravedad:
            self.vy += self.gravedad * dt

    def aplicar_desplazamiento_horizontal(self, dt: float):
        """2. Desplazamiento horizontal: Modifica la coordenada x según vx y delta time."""
        self.x += self.vx * dt

    def resolver_colisiones(self, obstaculos: list, dt: float):
        """4. Resolución de colisiones: Maneja colisiones en ambos ejes contra la lista de obstáculos."""
        if not obstaculos:
            self.y += self.vy * dt
            return

        # Colisión en Eje X
        self.hitbox.x = round(self.x)
        for obstaculo in obstaculos:
            if obstaculo is not self and hasattr(obstaculo, 'hitbox') and self.hitbox.colliderect(obstaculo.hitbox):
                if self.vx > 0:
                    self.hitbox.right = obstaculo.hitbox.left
                elif self.vx < 0:
                    self.hitbox.left = obstaculo.hitbox.right
                self.x = float(self.hitbox.x)
                self.vx = 0.0

        # Movimiento y Colisión en Eje Y
        self.y += self.vy * dt
        self.hitbox.y = round(self.y)
        for obstaculo in obstaculos:
            if obstaculo is not self and hasattr(obstaculo, 'hitbox') and self.hitbox.colliderect(obstaculo.hitbox):
                if self.vy > 0:
                    self.hitbox.bottom = obstaculo.hitbox.top
                elif self.vy < 0:
                    self.hitbox.top = obstaculo.hitbox.bottom
                self.y = float(self.hitbox.y)
                self.vy = 0.0

    def actualizar_posicion_espacial(self):
        """3. Actualización espacial: Sincroniza la posición de rect y hitbox con x e y."""
        self.rect.x = round(self.x)
        self.rect.y = round(self.y)
        self.hitbox.center = self.rect.center

    def actualizar(self, dt: float, obstaculos: list = None):
        """
        Método plantilla arquitectónico (Template Method Pattern).
        Ejecuta la secuencia de actualización en el orden requerido:
        1. Lógica interna específica de la entidad
        2. Caída libre (Gravedad)
        3. Desplazamiento horizontal (vx * dt)
        4. Resolución de colisiones
        5. Actualización espacial (rect y hitbox)
        """
        self.actualizar_logica(dt)
        self.aplicar_caida_libre(dt)
        self.aplicar_desplazamiento_horizontal(dt)
        self.resolver_colisiones(obstaculos, dt)
        self.actualizar_posicion_espacial()

    @abstractmethod
    def dibujar(self, pantalla: pygame.Surface, camara_offset: pygame.math.Vector2 = None):
        """Método abstracto para renderizar la entidad en pantalla."""
        if camara_offset:
            render_pos = (self.rect.x - int(camara_offset.x), self.rect.y - int(camara_offset.y))
        else:
            render_pos = self.rect.topleft
        pantalla.blit(self.image, render_pos)
