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
HEALTH_TEXT_COLOR = (255, 255, 255)  # Blanco para texto de salud en centro

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

# Física (velocidades reducidas 25% = *0.75; físicas más suaves: bounce_factor=0.8, parry=1.8)
BOUNCE_FACTOR = 0.8  # Reducido para rebotes más suaves
PARRY_BOUNCE = 1.8   # Aumentado para más impulso en parry (choque de armas)
IMPULSE_STRENGTH = 93.75  # 125 * 0.75
DECAY_TIME = 3.0     # Tiempo en segundos para decay de velocidad
MIN_BOUNCE_SPEED = 187.5  # 250 * 0.75
MIN_SPEED = 375           # 500 * 0.75
MAX_SPEED = 750           # 1000 * 0.75
GRAVITY = 0          # Sin gravedad por ahora
COLLISION_DAMPING = 0.9  # Damping para colisiones pelota-pelota más suaves
ATTRACTION_STRENGTH = 50  # Nueva: fuerza de atracción débil entre pelotas para más interacciones
HIT_COOLDOWN = 0.5  # Tiempo en segundos para evitar múltiples hits consecutivos entre misma pair
HIT_IMPULSE_FACTOR = 1.5  # Aumentado para impulso más fuerte en hits (reverse direction)

# FPS
FPS = 60
HEALTH_FONT_SIZE = 60  # 24 * 2.5 (tamaño de fuente escalado para salud en centro)
STATS_FONT_SIZE = 20   # Reducido para stats fuera (más pequeño)
ARENA_BORDER_THICKNESS = 2  # No escalado, ya que arena no cambia

# Posiciones fijas para stats fuera de la arena (lado izquierdo)
STATS_X = 20  # Izquierda de la pantalla
STATS_Y_START = 50  # Inicio vertical
STATS_Y_SPACING = 100  # Espacio entre stats de cada pelota (reducido para más compacto)

# Botón de reset
RESET_BUTTON_RECT = pygame.Rect(SCREEN_WIDTH - 150, 10, 140, 40)  # Posición en esquina superior derecha
RESET_BUTTON_COLOR = (100, 100, 100)  # Gris
RESET_BUTTON_TEXT_COLOR = (255, 255, 255)  # Blanco
RESET_BUTTON_FONT_SIZE = 24

# Color para outline de texto (negro para trazo)
OUTLINE_COLOR = (0, 0, 0)
OUTLINE_THICKNESS = 2  # Grosor del trazo

# Menú inicial
MENU_BUTTON_WIDTH = 200
MENU_BUTTON_HEIGHT = 50
MENU_BUTTON_SPACING = 20
MENU_BUTTON_COLOR = (150, 150, 150)
MENU_BUTTON_TEXT_COLOR = (0, 0, 0)
MENU_BUTTON_FONT_SIZE = 30
MENU_TITLE_FONT_SIZE = 40
MENU_TITLE_COLOR = (0, 0, 0)
START_BUTTON_RECT = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 100, 200, 50)
START_BUTTON_COLOR = (0, 200, 0)

# Spin speeds base aumentados x3 para rotación más rápida
SWORD_SPIN_BASE = 3  # 1 * 3
AXE_SPIN_BASE = 1.5  # 0.5 * 3
LANCE_SPIN_BASE = 15  # 5 * 3