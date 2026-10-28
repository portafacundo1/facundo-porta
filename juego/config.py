"""Constantes de configuración del juego."""

# Pantalla
ANCHO = 480
ALTO = 720
FPS = 60
TITULO = "Tráfico Loco"

# Ruta (4 carriles)
CARRILES = 4
RUTA_X = 60
RUTA_ANCHO = 360
ANCHO_CARRIL = RUTA_ANCHO // CARRILES

# Autos
AUTO_ANCHO = 42
AUTO_ALTO = 76
VEL_LATERAL = 6

# Dificultad
VEL_INICIAL = 5.0
VEL_MAX = 15.0
VIDAS = 3
FRAMES_INVULNERABLE = 90  # ~1.5 segundos

# Puntos
PUNTOS_MONEDA = 50

# Colores
VERDE_PASTO = (46, 125, 50)
ASFALTO = (55, 55, 60)
LINEA = (240, 240, 240)
BORDE = (230, 200, 40)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (220, 40, 40)
AMARILLO = (255, 215, 0)
COLORES_ENEMIGOS = [
    (30, 110, 220),
    (240, 140, 20),
    (150, 60, 190),
    (40, 170, 160),
    (200, 200, 200),
    (230, 90, 140),
]

ARCHIVO_RECORD = "record.txt"
