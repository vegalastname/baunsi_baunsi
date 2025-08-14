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
        self.health_font = pygame.font.SysFont(None, HEALTH_FONT_SIZE)  # Fuente escalada para salud
        self.stats_font = pygame.font.SysFont(None, STATS_FONT_SIZE)   # Fuente para stats adicionales
        self.balls = [
            Ball((ARENA_LEFT + 150, ARENA_TOP + 150), 'sword'),  # Ajustado para BALL_RADIUS=50
            Ball((ARENA_LEFT + 250, ARENA_TOP + 250), 'axe'),
            Ball((ARENA_LEFT + 350, ARENA_TOP + 350), 'lance')
        ]
        self.running = True

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0  # Delta time en segundos
            self.handle_events()
            self.update(dt)
            self.render()
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self, dt):
        # Actualizar todas las pelotas
        for ball in self.balls[:]:
            ball.update(dt)
            ball.bounce_wall()
            if not ball.is_alive():
                self.balls.remove(ball)

        # Manejar colisiones
        handle_collisions(self.balls)

    def render(self):
        self.screen.fill(BACKGROUND_COLOR)  # Fondo gris fuera de la arena
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

            # Dibujar texto de salud en el centro
            health_value = max(0, int(ball.weapon.health))  # Salud
            health_text = self.health_font.render(str(health_value), True, HEALTH_TEXT_COLOR)
            health_rect = health_text.get_rect(center=(int(ball.position[0]), int(ball.position[1])))
            self.screen.blit(health_text, health_rect)

            # Dibujar stats adicionales debajo de la salud (spin_speed, damage, calculated_damage)
            spin_speed = f"Spin: {ball.weapon.spin_speed:.1f}"
            damage = f"Dmg: {ball.weapon.damage:.1f}"
            calc_damage = f"Calc Dmg: {ball.weapon.calculate_damage():.1f}"
            stats_texts = [spin_speed, damage, calc_damage]

            y_offset = health_rect.bottom + 5  # Posicionar debajo de la salud (ajustado para fuentes más grandes)
            for stat in stats_texts:
                stat_text = self.stats_font.render(stat, True, HEALTH_TEXT_COLOR)
                stat_rect = stat_text.get_rect(center=(int(ball.position[0]), y_offset))
                self.screen.blit(stat_text, stat_rect)
                y_offset += stat_text.get_height() + 2  # Espacio entre líneas

        pygame.display.flip()