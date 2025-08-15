import math
import pygame
from constants import *
from entities import Ball
from physics import handle_collisions

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Arena Balls Game")
        self.clock = pygame.time.Clock()
        self.health_font = pygame.font.SysFont(None, HEALTH_FONT_SIZE)  # Fuente para salud en centro
        self.stats_font = pygame.font.SysFont(None, STATS_FONT_SIZE)   # Fuente más pequeña para stats fuera
        self.button_font = pygame.font.SysFont(None, RESET_BUTTON_FONT_SIZE)  # Fuente para botón
        self.menu_font = pygame.font.SysFont(None, MENU_BUTTON_FONT_SIZE)  # Fuente para menú
        self.title_font = pygame.font.SysFont(None, MENU_TITLE_FONT_SIZE)  # Fuente para título de menú
        self.state = "menu"  # Estados: "menu", "game"
        self.selected_balls = []  # Lista de weapon_types seleccionados (máx 2)
        self.hit_cooldowns = {}  # Diccionario para cooldowns de hits: key=(id(ball1), id(ball2)), value=last_hit_time
        self.running = True

    def reset_game(self):
        # Reiniciar pelotas basado en selected_balls
        if self.state == "game":
            positions = [(ARENA_LEFT + 150, ARENA_TOP + 250), (ARENA_LEFT + 350, ARENA_TOP + 250)]  # Dos posiciones centradas
            self.balls = [Ball(pos, typ) for pos, typ in zip(positions, self.selected_balls)]
            self.hit_cooldowns = {}  # Reset cooldowns

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0  # Delta time en segundos
            self.handle_events()
            if self.state == "game":
                self.update(dt)
            self.render()
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Click izquierdo
                    mouse_pos = pygame.mouse.get_pos()
                    if self.state == "menu":
                        # Botones de selección de pelotas
                        sword_rect = pygame.Rect(SCREEN_WIDTH // 2 - MENU_BUTTON_WIDTH - MENU_BUTTON_SPACING, SCREEN_HEIGHT // 2 - MENU_BUTTON_HEIGHT // 2, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)
                        axe_rect = pygame.Rect(SCREEN_WIDTH // 2 - MENU_BUTTON_WIDTH // 2, SCREEN_HEIGHT // 2 - MENU_BUTTON_HEIGHT // 2, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)
                        lance_rect = pygame.Rect(SCREEN_WIDTH // 2 + MENU_BUTTON_SPACING, SCREEN_HEIGHT // 2 - MENU_BUTTON_HEIGHT // 2, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)
                        if sword_rect.collidepoint(mouse_pos) and len(self.selected_balls) < 2 and 'sword' not in self.selected_balls:
                            self.selected_balls.append('sword')
                        elif axe_rect.collidepoint(mouse_pos) and len(self.selected_balls) < 2 and 'axe' not in self.selected_balls:
                            self.selected_balls.append('axe')
                        elif lance_rect.collidepoint(mouse_pos) and len(self.selected_balls) < 2 and 'lance' not in self.selected_balls:
                            self.selected_balls.append('lance')
                        # Botón Start
                        if START_BUTTON_RECT.collidepoint(mouse_pos) and len(self.selected_balls) == 2:
                            self.state = "game"
                            self.reset_game()
                    elif self.state == "game":
                        # Botón Reset
                        if RESET_BUTTON_RECT.collidepoint(mouse_pos):
                            self.state = "menu"
                            self.selected_balls = []

    def update(self, dt):
        # Actualizar todas las pelotas
        for ball in self.balls[:]:
            ball.update(dt)
            ball.bounce_wall()
            if not ball.is_alive():
                self.balls.remove(ball)

        # Manejar colisiones
        handle_collisions(self.balls, self)

        # Añadir atracción débil entre pelotas si hay exactamente 2
        if len(self.balls) == 2:
            ball1, ball2 = self.balls
            dx = ball2.position[0] - ball1.position[0]
            dy = ball2.position[1] - ball1.position[1]
            dist = math.sqrt(dx**2 + dy**2)
            if dist > 0:
                nx = dx / dist
                ny = dy / dist
                # Añadir aceleración hacia la otra (débil, decae)
                ball1.acceleration[0] += nx * ATTRACTION_STRENGTH * dt
                ball1.acceleration[1] += ny * ATTRACTION_STRENGTH * dt
                ball2.acceleration[0] -= nx * ATTRACTION_STRENGTH * dt
                ball2.acceleration[1] -= ny * ATTRACTION_STRENGTH * dt

    def render(self):
        self.screen.fill(BACKGROUND_COLOR)
        if self.state == "menu":
            # Dibujar título
            title_text = self.title_font.render("Select 2 Balls", True, MENU_TITLE_COLOR)
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
            self.screen.blit(title_text, title_rect)

            # Dibujar botones de selección
            sword_rect = pygame.Rect(SCREEN_WIDTH // 2 - MENU_BUTTON_WIDTH - MENU_BUTTON_SPACING, SCREEN_HEIGHT // 2 - MENU_BUTTON_HEIGHT // 2, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)
            axe_rect = pygame.Rect(SCREEN_WIDTH // 2 - MENU_BUTTON_WIDTH // 2, SCREEN_HEIGHT // 2 - MENU_BUTTON_HEIGHT // 2, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)
            lance_rect = pygame.Rect(SCREEN_WIDTH // 2 + MENU_BUTTON_SPACING, SCREEN_HEIGHT // 2 - MENU_BUTTON_HEIGHT // 2, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)

            pygame.draw.rect(self.screen, MENU_BUTTON_COLOR, sword_rect)
            sword_text = self.menu_font.render("Sword", True, MENU_BUTTON_TEXT_COLOR)
            self.screen.blit(sword_text, (sword_rect.centerx - sword_text.get_width() // 2, sword_rect.centery - sword_text.get_height() // 2))

            pygame.draw.rect(self.screen, MENU_BUTTON_COLOR, axe_rect)
            axe_text = self.menu_font.render("Axe", True, MENU_BUTTON_TEXT_COLOR)
            self.screen.blit(axe_text, (axe_rect.centerx - axe_text.get_width() // 2, axe_rect.centery - axe_text.get_height() // 2))

            pygame.draw.rect(self.screen, MENU_BUTTON_COLOR, lance_rect)
            lance_text = self.menu_font.render("Lance", True, MENU_BUTTON_TEXT_COLOR)
            self.screen.blit(lance_text, (lance_rect.centerx - lance_text.get_width() // 2, lance_rect.centery - lance_text.get_height() // 2))

            # Dibujar seleccionadas
            selected_text = self.menu_font.render(f"Selected: {', '.join(self.selected_balls)}", True, MENU_TITLE_COLOR)
            self.screen.blit(selected_text, (SCREEN_WIDTH // 2 - selected_text.get_width() // 2, SCREEN_HEIGHT // 2 + 100))

            # Botón Start (solo si 2 seleccionadas)
            if len(self.selected_balls) == 2:
                pygame.draw.rect(self.screen, START_BUTTON_COLOR, START_BUTTON_RECT)
                start_text = self.menu_font.render("Start", True, MENU_BUTTON_TEXT_COLOR)
                start_rect = start_text.get_rect(center=START_BUTTON_RECT.center)
                self.screen.blit(start_text, start_rect)
        else:  # state == "game"
            # Dibujar la arena (cuadrado blanco con borde negro)
            pygame.draw.rect(self.screen, ARENA_COLOR, (ARENA_LEFT, ARENA_TOP, ARENA_WIDTH, ARENA_HEIGHT))
            pygame.draw.rect(self.screen, ARENA_BORDER_COLOR, (ARENA_LEFT, ARENA_TOP, ARENA_WIDTH, ARENA_HEIGHT), ARENA_BORDER_THICKNESS)

            for ball in self.balls:
                # Dibujar pelota con color único
                pygame.draw.circle(self.screen, ball.color, (int(ball.position[0]), int(ball.position[1])), BALL_RADIUS)
                # Dibujar arma (línea con grosor escalado)
                start = (int(ball.position[0]), int(ball.position[1]))
                end = ball.weapon.get_end_point()
                pygame.draw.line(self.screen, WEAPON_COLOR, start, (int(end[0]), int(end[1])), WEAPON_THICKNESS)

                # Dibujar texto de salud en el centro de la pelota
                health_value = max(0, int(ball.weapon.health))
                health_text = self.health_font.render(str(health_value), True, HEALTH_TEXT_COLOR)
                health_rect = health_text.get_rect(center=(int(ball.position[0]), int(ball.position[1])))
                self.screen.blit(health_text, health_rect)

            # Dibujar stats fuera de la arena (lado izquierdo, posiciones fijas por tipo de arma)
            y_pos = STATS_Y_START
            for ball in self.balls:
                if not ball.is_alive():
                    continue  # No mostrar stats si muerta

                # Color de texto = color de la pelota
                text_color = ball.color

                # Stats adicionales (pequeñas con outline)
                spin_speed = f"Spin: {ball.weapon.spin_speed:.1f}"
                damage = f"Dmg: {ball.weapon.damage:.1f}"
                calc_damage = f"Calc Dmg: {ball.weapon.calculate_damage():.1f}"
                stats_texts = [spin_speed, damage, calc_damage]

                for stat in stats_texts:
                    # Dibujar outline (renderizar texto en negro desplazado)
                    for dx in range(-OUTLINE_THICKNESS, OUTLINE_THICKNESS + 1):
                        for dy in range(-OUTLINE_THICKNESS, OUTLINE_THICKNESS + 1):
                            if dx == 0 and dy == 0:
                                continue  # Saltar el centro
                            outline_text = self.stats_font.render(stat, True, OUTLINE_COLOR)
                            self.screen.blit(outline_text, (STATS_X + dx, y_pos + dy))

                    # Dibujar texto principal
                    stat_text = self.stats_font.render(stat, True, text_color)
                    self.screen.blit(stat_text, (STATS_X, y_pos))
                    y_pos += stat_text.get_height() + 2

                y_pos += 20  # Espacio extra entre pelotas

            # Dibujar botón de reset
            pygame.draw.rect(self.screen, RESET_BUTTON_COLOR, RESET_BUTTON_RECT)
            reset_text = self.button_font.render("Reset", True, RESET_BUTTON_TEXT_COLOR)
            reset_rect = reset_text.get_rect(center=RESET_BUTTON_RECT.center)
            self.screen.blit(reset_text, reset_rect)

        pygame.display.flip()