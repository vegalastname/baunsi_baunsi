import math
import random
import pygame
from constants import *

class Weapon:
    def __init__(self, ball, damage_base, health_base, spin_speed_base):
        self.ball = ball  # Referencia a la pelota dueña
        self.damage = damage_base
        self.spin_speed = spin_speed_base
        self.angle = 0  # Ángulo de rotación inicial
        self.health = health_base  # Salud de la entidad (pelota + arma)
        self.length = 0  # Longitud del arma (sobrescrita en subclases)

    def update(self, dt):
        # Rotar el arma
        self.angle = (self.angle + self.spin_speed * dt) % (2 * math.pi)

    def get_end_point(self):
        # Calcular punto final del arma (línea desde centro de pelota)
        center = self.ball.position
        end_x = center[0] + self.length * math.cos(self.angle)
        end_y = center[1] + self.length * math.sin(self.angle)
        return (end_x, end_y)

    def on_hit(self):
        # Método abstracto: efectos al golpear
        pass

    def calculate_damage(self):
        # Fórmula: (1/3 * damage) * (1/2 * spin_speed)
        return (self.damage / 3) * (self.spin_speed / 2)

class Sword(Weapon):
    def __init__(self, ball):
        super().__init__(ball, damage_base=5, health_base=100, spin_speed_base=SWORD_SPIN_BASE)
        self.length = SWORD_LENGTH

    def on_hit(self):
        self.damage += 1

class Axe(Weapon):
    def __init__(self, ball):
        super().__init__(ball, damage_base=10, health_base=125, spin_speed_base=AXE_SPIN_BASE)
        self.length = AXE_LENGTH

    def on_hit(self):
        self.damage += 0.5
        self.spin_speed += 0.75

class Lance(Weapon):
    def __init__(self, ball):
        super().__init__(ball, damage_base=2, health_base=75, spin_speed_base=LANCE_SPIN_BASE)
        self.length = LANCE_LENGTH

    def on_hit(self):
        self.spin_speed += 0.01

class Ball:
    def __init__(self, position, weapon_type):
        self.weapon_type = weapon_type  # Para identificar en render
        # Asegurar posición inicial dentro de la arena
        self.position = [
            max(ARENA_LEFT + BALL_RADIUS, min(position[0], ARENA_LEFT + ARENA_WIDTH - BALL_RADIUS)),
            max(ARENA_TOP + BALL_RADIUS, min(position[1], ARENA_TOP + ARENA_HEIGHT - BALL_RADIUS))
        ]
        # Generar base_velocity con magnitude entre MIN_SPEED y MAX_SPEED, dirección aleatoria
        speed = random.uniform(MIN_SPEED, MAX_SPEED)
        angle = random.uniform(0, 2 * math.pi)
        self.base_velocity = [speed * math.cos(angle), speed * math.sin(angle)]
        self.acceleration = [0, 0]  # Aceleración temporal (modificada solo por colisiones)
        self.last_hit_time = -float('inf')  # Tiempo del último golpe (en s)
        if weapon_type == 'sword':
            self.weapon = Sword(self)
            self.color = SWORD_COLOR
        elif weapon_type == 'axe':
            self.weapon = Axe(self)
            self.color = AXE_COLOR
        elif weapon_type == 'lance':
            self.weapon = Lance(self)
            self.color = LANCE_COLOR
        else:
            raise ValueError("Tipo de arma inválido")

    def update(self, dt):
        # Calcular velocidad total
        vx = self.base_velocity[0] + self.acceleration[0]
        vy = self.base_velocity[1] + self.acceleration[1]

        # Actualizar posición
        self.position[0] += vx * dt
        self.position[1] += vy * dt

        # Actualizar arma
        self.weapon.update(dt)

        # Decay de aceleración si ha pasado tiempo desde el último golpe
        current_time = pygame.time.get_ticks() / 1000.0  # Tiempo en segundos
        time_since_hit = current_time - self.last_hit_time
        if time_since_hit > 0 and time_since_hit <= DECAY_TIME:
            # Lerp gradual de aceleración hacia [0,0] durante DECAY_TIME
            lerp_factor = dt / DECAY_TIME  # Porción de decay por frame
            self.acceleration[0] = self.acceleration[0] * (1 - lerp_factor)
            self.acceleration[1] = self.acceleration[1] * (1 - lerp_factor)
        elif time_since_hit > DECAY_TIME:
            self.acceleration = [0, 0]  # Set directo a 0 si >3s

    def bounce_wall(self):
        x_bounced = False
        y_bounced = False

        # Rebote X
        if self.position[0] - BALL_RADIUS < ARENA_LEFT:
            self.position[0] = ARENA_LEFT + BALL_RADIUS
            self.base_velocity[0] *= -BOUNCE_FACTOR
            self.acceleration[0] *= -BOUNCE_FACTOR  # Invertir aceleración para conservar momentum
            if abs(self.base_velocity[0]) < MIN_BOUNCE_SPEED:
                self.base_velocity[0] = MIN_BOUNCE_SPEED if self.base_velocity[0] > 0 else -MIN_BOUNCE_SPEED
            x_bounced = True
        elif self.position[0] + BALL_RADIUS > ARENA_LEFT + ARENA_WIDTH:
            self.position[0] = ARENA_LEFT + ARENA_WIDTH - BALL_RADIUS
            self.base_velocity[0] *= -BOUNCE_FACTOR
            self.acceleration[0] *= -BOUNCE_FACTOR  # Invertir aceleración
            if abs(self.base_velocity[0]) < MIN_BOUNCE_SPEED:
                self.base_velocity[0] = MIN_BOUNCE_SPEED if self.base_velocity[0] > 0 else -MIN_BOUNCE_SPEED
            x_bounced = True

        # Rebote Y
        if self.position[1] - BALL_RADIUS < ARENA_TOP:
            self.position[1] = ARENA_TOP + BALL_RADIUS
            self.base_velocity[1] *= -BOUNCE_FACTOR
            self.acceleration[1] *= -BOUNCE_FACTOR  # Invertir aceleración
            if abs(self.base_velocity[1]) < MIN_BOUNCE_SPEED:
                self.base_velocity[1] = MIN_BOUNCE_SPEED if self.base_velocity[1] > 0 else -MIN_BOUNCE_SPEED
            y_bounced = True
        elif self.position[1] + BALL_RADIUS > ARENA_TOP + ARENA_HEIGHT:
            self.position[1] = ARENA_TOP + ARENA_HEIGHT - BALL_RADIUS
            self.base_velocity[1] *= -BOUNCE_FACTOR
            self.acceleration[1] *= -BOUNCE_FACTOR  # Invertir aceleración
            if abs(self.base_velocity[1]) < MIN_BOUNCE_SPEED:
                self.base_velocity[1] = MIN_BOUNCE_SPEED if self.base_velocity[1] > 0 else -MIN_BOUNCE_SPEED
            y_bounced = True

        # Si rebote en esquina (ambos axes), agregar impulso extra en aceleración para salir
        if x_bounced and y_bounced:
            # Determinar dirección de push basada en esquina
            push_x = MIN_BOUNCE_SPEED if self.position[0] < ARENA_LEFT + ARENA_SIZE / 2 else -MIN_BOUNCE_SPEED
            push_y = MIN_BOUNCE_SPEED if self.position[1] < ARENA_TOP + ARENA_SIZE / 2 else -MIN_BOUNCE_SPEED
            self.acceleration[0] += push_x
            self.acceleration[1] += push_y

    def apply_damage(self, damage):
        self.weapon.health = max(0, self.weapon.health - damage)  # Solo restar salud
        self.last_hit_time = pygame.time.get_ticks() / 1000.0  # Reset timer de decay al ser golpeado
        if self.weapon.health <= 0:
            self.base_velocity = [0, 0]
            self.acceleration = [0, 0]

    def is_alive(self):
        return self.weapon.health > 0