"""Lógica principal del juego: estados, bucle, dibujo y colisiones."""
import os
import random
import sys

import pygame

from . import config as c
from .entidades import Enemigo, Jugador, Moneda


class Juego:
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((c.ANCHO, c.ALTO))
        pygame.display.set_caption(c.TITULO)
        self.reloj = pygame.time.Clock()
        self.fuente = pygame.font.SysFont("arial", 22, bold=True)
        self.fuente_media = pygame.font.SysFont("arial", 28, bold=True)
        self.fuente_grande = pygame.font.SysFont("arial", 52, bold=True)
        self.record = self._cargar_record()
        self.estado = "menu"  # menu | jugando | gameover
        self.reiniciar()

    # ------------------------------------------------------------ estado
    def reiniciar(self):
        self.jugador = Jugador()
        self.enemigos = []
        self.monedas = []
        self.puntaje = 0.0
        self.monedas_juntadas = 0
        self.vidas = c.VIDAS
        self.velocidad = c.VEL_INICIAL
        self.offset_lineas = 0.0
        self.timer_enemigo = 0
        self.timer_moneda = 0
        self.invulnerable = 0
        self.pausa = False
        self.nuevo_record = False

    def _cargar_record(self):
        try:
            with open(c.ARCHIVO_RECORD, "r", encoding="utf-8") as f:
                return int(f.read().strip())
        except (OSError, ValueError):
            return 0

    def _guardar_record(self):
        try:
            with open(c.ARCHIVO_RECORD, "w", encoding="utf-8") as f:
                f.write(str(self.record))
        except OSError:
            pass

    # ------------------------------------------------------------ bucle
    def ejecutar(self):
        while True:
            self._eventos()
            self._actualizar()
            self._dibujar()
            pygame.display.flip()
            self.reloj.tick(c.FPS)

    def _eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self._salir()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self._salir()
                if evento.key in (pygame.K_RETURN, pygame.K_SPACE):
                    if self.estado == "menu":
                        self.estado = "jugando"
                    elif self.estado == "gameover":
                        self.reiniciar()
                        self.estado = "jugando"
                if evento.key == pygame.K_p and self.estado == "jugando":
                    self.pausa = not self.pausa

    def _salir(self):
        pygame.quit()
        sys.exit()

    # ------------------------------------------------------------ lógica
    def _actualizar(self):
        if self.estado != "jugando" or self.pausa:
            return

        self.jugador.mover(pygame.key.get_pressed())

        # La velocidad sube con el puntaje
        self.velocidad = min(c.VEL_MAX, c.VEL_INICIAL + self.puntaje / 1500)
        self.puntaje += self.velocidad * 0.1
        self.offset_lineas = (self.offset_lineas + self.velocidad) % 60

        # Aparición de enemigos y monedas
        self.timer_enemigo += 1
        if self.timer_enemigo >= max(20, int(300 / self.velocidad)):
            self.timer_enemigo = 0
            self.enemigos.append(Enemigo(self.velocidad))

        self.timer_moneda += 1
        if self.timer_moneda >= 140:
            self.timer_moneda = 0
            if random.random() < 0.8:
                self.monedas.append(Moneda())

        for e in self.enemigos:
            e.actualizar(self.velocidad)
        for m in self.monedas:
            m.actualizar(self.velocidad)
        self.enemigos = [e for e in self.enemigos if not e.fuera_de_pantalla()]
        self.monedas = [m for m in self.monedas if not m.fuera_de_pantalla()]

        self._colisiones()

        if self.invulnerable > 0:
            self.invulnerable -= 1

    def _colisiones(self):
        hit = self.jugador.hitbox

        # Monedas
        for m in self.monedas[:]:
            if hit.colliderect(m.rect):
                self.monedas.remove(m)
                self.monedas_juntadas += 1
                self.puntaje += c.PUNTOS_MONEDA

        # Choques
        if self.invulnerable == 0:
            for e in self.enemigos[:]:
                if hit.colliderect(e.hitbox):
                    self.enemigos.remove(e)
                    self.vidas -= 1
                    self.invulnerable = c.FRAMES_INVULNERABLE
                    if self.vidas <= 0:
                        self._terminar()
                    break

    def _terminar(self):
        self.estado = "gameover"
        if int(self.puntaje) > self.record:
            self.record = int(self.puntaje)
            self.nuevo_record = True
            self._guardar_record()

    # ------------------------------------------------------------ dibujo
    def _texto(self, texto, fuente, color, centro=None, topleft=None, topright=None):
        img = fuente.render(texto, True, color)
        rect = img.get_rect()
        if centro:
            rect.center = centro
        if topleft:
            rect.topleft = topleft
        if topright:
            rect.topright = topright
        self.pantalla.blit(img, rect)

    def _dibujar_ruta(self):
        self.pantalla.fill(c.VERDE_PASTO)
        ruta = pygame.Rect(c.RUTA_X, 0, c.RUTA_ANCHO, c.ALTO)
        pygame.draw.rect(self.pantalla, c.ASFALTO, ruta)
        pygame.draw.rect(self.pantalla, c.BORDE, (c.RUTA_X - 4, 0, 4, c.ALTO))
        pygame.draw.rect(self.pantalla, c.BORDE, (c.RUTA_X + c.RUTA_ANCHO, 0, 4, c.ALTO))
        # Líneas de carril discontinuas que se mueven
        for i in range(1, c.CARRILES):
            x = c.RUTA_X + i * c.ANCHO_CARRIL
            y = -60 + self.offset_lineas
            while y < c.ALTO:
                pygame.draw.rect(self.pantalla, c.LINEA, (x - 2, y, 4, 30))
                y += 60

    def _dibujar_hud(self):
        self._texto(f"Puntos: {int(self.puntaje)}", self.fuente, c.BLANCO, topleft=(10, 10))
        self._texto(f"Récord: {self.record}", self.fuente, c.BLANCO, topleft=(10, 38))
        self._texto(f"Vidas: {'♥' * self.vidas}", self.fuente, c.ROJO, topright=(c.ANCHO - 10, 10))
        kmh = int(self.velocidad * 14)
        self._texto(f"{kmh} km/h", self.fuente, c.BLANCO, topright=(c.ANCHO - 10, 38))

    def _dibujar(self):
        self._dibujar_ruta()

        if self.estado == "menu":
            self._pantalla_menu()
            return

        for m in self.monedas:
            m.dibujar(self.pantalla)
        for e in self.enemigos:
            e.dibujar(self.pantalla)
        parpadeo = self.invulnerable > 0 and (self.invulnerable // 6) % 2 == 0
        self.jugador.dibujar(self.pantalla, parpadeo)
        self._dibujar_hud()

        if self.pausa:
            self._cartel(["PAUSA", "Apretá P para seguir"])
        elif self.estado == "gameover":
            lineas = ["GAME OVER", f"Puntos: {int(self.puntaje)}  |  Monedas: {self.monedas_juntadas}"]
            if self.nuevo_record:
                lineas.append("¡Nuevo récord!")
            lineas.append("ENTER para jugar de nuevo")
            self._cartel(lineas)

    def _cartel(self, lineas):
        velo = pygame.Surface((c.ANCHO, c.ALTO), pygame.SRCALPHA)
        velo.fill((0, 0, 0, 160))
        self.pantalla.blit(velo, (0, 0))
        y = c.ALTO // 2 - 60
        for i, linea in enumerate(lineas):
            fuente = self.fuente_grande if i == 0 else self.fuente
            self._texto(linea, fuente, c.BLANCO, centro=(c.ANCHO // 2, y))
            y += 60 if i == 0 else 36

    def _pantalla_menu(self):
        velo = pygame.Surface((c.ANCHO, c.ALTO), pygame.SRCALPHA)
        velo.fill((0, 0, 0, 150))
        self.pantalla.blit(velo, (0, 0))
        self._texto("TRÁFICO LOCO", self.fuente_grande, c.AMARILLO, centro=(c.ANCHO // 2, 190))
        self._texto("Esquivá los autos y juntá monedas", self.fuente, c.BLANCO, centro=(c.ANCHO // 2, 260))
        instrucciones = [
            "← → o A D : mover el auto",
            "P : pausa",
            "ESC : salir",
        ]
        for i, t in enumerate(instrucciones):
            self._texto(t, self.fuente, c.BLANCO, centro=(c.ANCHO // 2, 340 + i * 34))
        self._texto("ENTER para empezar", self.fuente_media, c.AMARILLO, centro=(c.ANCHO // 2, 520))
        self._texto(f"Récord: {self.record}", self.fuente, c.BLANCO, centro=(c.ANCHO // 2, 580))
