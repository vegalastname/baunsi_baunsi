import pygame

# Dimensiones (no escaladas)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (200, 200, 200)  # Gris claro para fondo fuera de la arena
ARENA_COLOR = (255, 255, 255)  # Blanco para el interior de la arena
ARENA_BORDER_COLOR = (0, 0, 0)  # Negro para el borde
ARENA_SIZE = 500  # No escalado
ARENA_LEFT = (SCREEN_WIDTH - ARENA_SIZE) // 2  # Centrado horizontal: 150
ARENA_TOP = (SCREEN_HEIGHT - ARENA_SIZE) // 2  # Centrado vertical: 50
ARENA_WIDTH = ARENA_SIZE
ARENA_HEIGHT = ARENA_SIZE
BALL_RADIUS = 50  # 20 * 2.5 - Solo pelota escalada
HEALTH_TEXT_COLOR = (255, 255, 255)  # Blanco para texto de salud

# Colores por tipo de pelota
SWORD_COLOR = (255, 0, 0)    # Rojo
AXE_COLOR = (0, 255, 0)      # Verde
LANCE_COLOR = (0, 0, 255)    # Azul

# Armas (longitudes escaladas x2.5)
SWORD_LENGTH = 100  # 40 * 2.5
AXE_LENGTH = 75     # 30 * 2.5
LANCE_LENGTH = 150  # 60 * 2.5
WEAPON_COLOR = (255, 0, 0)
WEAPON_THICKNESS = 13  # 5 * 2.5 (grosor de línea escalado)

# Física (velocidades e impulsos escalados x2.5 para proporcionalidad con tamaños mayores)
BOUNCE_FACTOR = 1.0  # Rebote elástico perfecto para mantener velocidad
PARRY_BOUNCE = 1.5   # Impulso extra en parry
IMPULSE_STRENGTH = 125  # 50 * 2.5 - Fuerza de impulso al ser golpeado (ajustable)
DECAY_TIME = 3.0     # Tiempo en segundos para decay de velocidad
MIN_BOUNCE_SPEED = 250  # 100 * 2.5 - Velocidad mínima después de rebote
MIN_SPEED = 500         # 200 * 2.5 - Magnitude mínima para velocidad base
MAX_SPEED = 1000        # 400 * 2.5 - Magnitude máxima para velocidad base
GRAVITY = 0          # Sin gravedad por ahora

# FPS
FPS = 60
HEALTH_FONT_SIZE = 60  # 24 * 2.5 (tamaño de fuente escalado para stats)
STATS_FONT_SIZE = 30   # Nuevo: fuente más pequeña para stats adicionales
ARENA_BORDER_THICKNESS = 2  # No escalado, ya que arena no cambia