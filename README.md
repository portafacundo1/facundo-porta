# 🚗 Tráfico Loco

Juego de autos hecho en **Python** con **pygame**. Manejás un auto rojo en una ruta de 4 carriles,
esquivás los autos que vienen en contra y juntás monedas. Cuanto más avanzás, más rápido va todo.

## Cómo ejecutarlo

1. Tener Python 3.9 o superior.
2. Instalar las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Correr el juego:
   ```bash
   python main.py
   ```

## Controles

| Tecla | Acción |
|-------|--------|
| ← / → o A / D | Mover el auto |
| ENTER / ESPACIO | Empezar / jugar de nuevo |
| P | Pausa |
| ESC | Salir |

## Reglas

- Empezás con **3 vidas**. Cada choque te saca una (y quedás invulnerable un ratito).
- Cada moneda suma **50 puntos**; avanzar también suma puntos.
- La velocidad aumenta con el puntaje.
- El mejor puntaje se guarda en `record.txt`.

## Estructura del proyecto

```
juego-autos/
├── main.py            # punto de entrada
├── requirements.txt   # dependencias
├── README.md
└── juego/
    ├── config.py      # constantes (pantalla, colores, dificultad)
    ├── entidades.py   # Jugador, Enemigo, Moneda y dibujo de autos
    └── juego.py       # bucle principal, estados, colisiones, HUD
```

No usa imágenes ni sonidos externos: todo se dibuja con formas de pygame.
