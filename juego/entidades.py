"""Clases de los objetos del juego: jugador, autos enemigos y monedas."""
import random

import pygame

from . import config as c


def centro_carril(indice):
    """Devuelve la coordenada X del centro de un carril."""
    return c.RUTA_X + indice * c.ANCHO_CARRIL + c.ANCHO_CARRIL // 2


def dibujar_auto(pantalla, rect, color, mirando_arriba=True):
    """Dibuja un auto visto desde arriba usando solo formas de pygame."""
    # Ruedas
    rueda_w, rueda_h = 7, 16
    for dx in (-3, rect.width - rueda_w + 3):
        for dy in (10, rect.height - rueda_h - 10):
            pygame.draw.rect(
                pantalla, c.NEGRO, (rect.x + dx, rect.y + dy, rueda_w, rueda_h),
                border_radius=2,
            )
    # Carrocería
    pygame.draw.rect(pantalla, color, rect, border_radius=10)
    # Techo y vidrios
    techo = pygame.Rect(rect.x + 6, rect.y + rect.height * 0.28, rect.width - 12, rect.height * 0.4)
    pygame.draw.rect(pantalla, (30, 40, 55), techo, border_radius=5)
    # Parabrisas (adelante) más claro
    if mirando_arriba:
        parabrisas = pygame.Rect(rect.x + 7, rect.y + rect.height * 0.28, rect.width - 14, 10)
    else:
        parabrisas = pygame.Rect(rect.x + 7, rect.y + rect.height * 0.68 - 10, rect.width - 14, 10)
    pygame.draw.rect(pantalla, (140, 190, 230), parabrisas, border_radius=3)
    # Luces
    y_luces = rect.y + 3 if mirando_arriba else rect.bottom - 8
    color_luz = (255, 250, 180) if mirando_arriba else (255, 70, 70)
    pygame.draw.rect(pantalla, color_luz, (rect.x + 4, y_luces, 9, 5), border_radius=2)
    pygame.draw.rect(pantalla, color_luz, (rect.right - 13, y_luces, 9, 5), border_radius=2)


class Jugador:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, c.AUTO_ANCHO, c.AUTO_ALTO)
        self.rect.centerx = centro_carril(c.CARRILES // 2)
        self.rect.bottom = c.ALTO - 30

    def mover(self, teclas):
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.rect.x -= c.VEL_LATERAL
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.rect.x += c.VEL_LATERAL
        # No salirse de la ruta
        self.rect.left = max(self.rect.left, c.RUTA_X + 4)
        self.rect.right = min(self.rect.right, c.RUTA_X + c.RUTA_ANCHO - 4)

    @property
    def hitbox(self):
        return self.rect.inflate(-8, -10)

    def dibujar(self, pantalla, parpadeo=False):
        if parpadeo:
            return  # no se dibuja en frames alternos para el efecto de parpadeo
        dibujar_auto(pantalla, self.rect, c.ROJO, mirando_arriba=True)


class Enemigo:
    """Auto que viene en sentido contrario."""

    def __init__(self, velocidad_ruta):
        carril = random.randrange(c.CARRILES)
        self.rect = pygame.Rect(0, 0, c.AUTO_ANCHO, c.AUTO_ALTO)
        self.rect.centerx = centro_carril(carril)
        self.y = float(-c.AUTO_ALTO - 10)
        self.rect.y = int(self.y)
        self.extra = random.uniform(1.0, 3.0)
        self.color = random.choice(c.COLORES_ENEMIGOS)

    def actualizar(self, velocidad_ruta):
        self.y += velocidad_ruta + self.extra
        self.rect.y = int(self.y)

    @property
    def hitbox(self):
        return self.rect.inflate(-8, -10)

    def fuera_de_pantalla(self):
        return self.rect.top > c.ALTO

    def dibujar(self, pantalla):
        dibujar_auto(pantalla, self.rect, self.color, mirando_arriba=False)


class Moneda:
    def __init__(self):
        self.radio = 12
        self.x = centro_carril(random.randrange(c.CARRILES))
        self.y = float(-self.radio * 2)
        self.rect = pygame.Rect(0, 0, self.radio * 2, self.radio * 2)
        self.rect.center = (self.x, int(self.y))

    def actualizar(self, velocidad_ruta):
        self.y += velocidad_ruta
        self.rect.center = (self.x, int(self.y))

    def fuera_de_pantalla(self):
        return self.rect.top > c.ALTO

    def dibujar(self, pantalla):
        pygame.draw.circle(pantalla, c.AMARILLO, self.rect.center, self.radio)
        pygame.draw.circle(pantalla, (200, 160, 0), self.rect.center, self.radio, 3)
        pygame.draw.circle(pantalla, (200, 160, 0), self.rect.center, self.radio // 3)
