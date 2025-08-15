import math
import pygame
from constants import *
from entities import Ball
from constants import BALL_RADIUS, PARRY_BOUNCE, IMPULSE_STRENGTH, MIN_BOUNCE_SPEED, COLLISION_DAMPING, HIT_COOLDOWN, HIT_IMPULSE_FACTOR

def line_line_intersection(p1, p2, p3, p4):
    # Detectar si dos líneas (p1-p2 y p3-p4) se intersectan
    # Implementación estándar de intersección de segmentos
    def ccw(A, B, C):
        return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])

    return ccw(p1, p3, p4) != ccw(p2, p3, p4) and ccw(p1, p2, p3) != ccw(p1, p2, p4)

def circle_line_intersection(circle_center, radius, line_start, line_end):
    # Detectar si segmento de línea intersecta círculo
    dx = line_end[0] - line_start[0]
    dy = line_end[1] - line_start[1]
    fx = line_start[0] - circle_center[0]
    fy = line_start[1] - circle_center[1]

    a = dx**2 + dy**2
    b = 2 * (fx * dx + fy * dy)
    c = fx**2 + fy**2 - radius**2

    discriminant = b**2 - 4 * a * c
    if discriminant < 0:
        return False

    discriminant = math.sqrt(discriminant)
    t1 = (-b - discriminant) / (2 * a)
    t2 = (-b + discriminant) / (2 * a)

    # Verificar si al menos un punto de intersección está en el segmento [0,1]
    if t1 >= 0 and t1 <= 1:
        return True
    if t2 >= 0 and t2 <= 1:
        return True
    return False

def handle_collisions(balls, game):  # Agregar game para hit_cooldowns
    for i in range(len(balls)):
        for j in range(i + 1, len(balls)):
            ball1 = balls[i]
            ball2 = balls[j]

            # Chequear colisión directa entre pelotas (círculo-círculo)
            dx = ball2.position[0] - ball1.position[0]
            dy = ball2.position[1] - ball1.position[1]
            dist = math.sqrt(dx**2 + dy**2)
            if dist < 2 * BALL_RADIUS:
                # Normalizar dirección
                if dist == 0:
                    dist = 0.001  # Evitar división por cero
                nx = dx / dist
                ny = dy / dist

                # Separar posiciones para evitar overlap
                overlap = 2 * BALL_RADIUS - dist
                ball1.position[0] -= nx * overlap / 2
                ball1.position[1] -= ny * overlap / 2
                ball2.position[0] += nx * overlap / 2
                ball2.position[1] += ny * overlap / 2

                # Rebote elástico en aceleración con damping para suavidad
                v1 = (ball1.base_velocity[0] + ball1.acceleration[0]) * nx + (ball1.base_velocity[1] + ball1.acceleration[1]) * ny
                v2 = (ball2.base_velocity[0] + ball2.acceleration[0]) * nx + (ball2.base_velocity[1] + ball2.acceleration[1]) * ny
                new_v1 = v2 * COLLISION_DAMPING
                new_v2 = v1 * COLLISION_DAMPING
                dv1 = (new_v1 - v1)
                dv2 = (new_v2 - v2)
                ball1.acceleration[0] += dv1 * nx
                ball1.acceleration[1] += dv1 * ny
                ball2.acceleration[0] += dv2 * nx
                ball2.acceleration[1] += dv2 * ny

                # Asegurar min speed relativa para evitar temblor (agregar a accel)
                rel_v = math.sqrt(((ball1.base_velocity[0] + ball1.acceleration[0]) - (ball2.base_velocity[0] + ball2.acceleration[0]))**2 + ((ball1.base_velocity[1] + ball1.acceleration[1]) - (ball2.base_velocity[1] + ball2.acceleration[1]))**2)
                if rel_v < MIN_BOUNCE_SPEED:
                    boost = (MIN_BOUNCE_SPEED - rel_v) / 2
                    ball1.acceleration[0] -= nx * boost
                    ball1.acceleration[1] -= ny * boost
                    ball2.acceleration[0] += nx * boost
                    ball2.acceleration[1] += ny * boost

                # No daño, solo repeler

            # Obtener líneas de armas
            weapon1_start = ball1.position
            weapon1_end = ball1.weapon.get_end_point()
            weapon2_start = ball2.position
            weapon2_end = ball2.weapon.get_end_point()

            # Chequear parry (arma vs arma)
            if line_line_intersection(weapon1_start, weapon1_end, weapon2_start, weapon2_end):
                # Parry: rebote (invertir velocidades con impulso en accel)
                ball1.acceleration[0] *= -PARRY_BOUNCE
                ball1.acceleration[1] *= -PARRY_BOUNCE
                ball2.acceleration[0] *= -PARRY_BOUNCE
                ball2.acceleration[1] *= -PARRY_BOUNCE

            # Cooldown check para daño
            pair_key = tuple(sorted([id(ball1), id(ball2)]))
            current_time = pygame.time.get_ticks() / 1000.0
            if pair_key in game.hit_cooldowns and current_time - game.hit_cooldowns[pair_key] < HIT_COOLDOWN:
                continue  # Saltar daño si en cooldown

            # Chequear daño: arma1 toca ball2
            if circle_line_intersection(ball2.position, BALL_RADIUS, weapon1_start, weapon1_end):
                damage = ball1.weapon.calculate_damage()
                ball2.apply_damage(damage)
                ball1.weapon.on_hit()  # Activar efecto on_hit
                # Impulso para atacante (hacia atrás: - su dirección)
                v_magnitude1 = math.sqrt(ball1.base_velocity[0]**2 + ball1.base_velocity[1]**2)
                if v_magnitude1 > 0:
                    nx1 = ball1.base_velocity[0] / v_magnitude1
                    ny1 = ball1.base_velocity[1] / v_magnitude1
                    ball1.acceleration[0] -= nx1 * HIT_IMPULSE_FACTOR * v_magnitude1
                    ball1.acceleration[1] -= ny1 * HIT_IMPULSE_FACTOR * v_magnitude1

                # Impulso para atacada (hacia delante: contraria a su dirección, i.e. reverse)
                v_magnitude2 = math.sqrt(ball2.base_velocity[0]**2 + ball2.base_velocity[1]**2)
                if v_magnitude2 > 0:
                    nx2 = ball2.base_velocity[0] / v_magnitude2
                    ny2 = ball2.base_velocity[1] / v_magnitude2
                    ball2.acceleration[0] -= nx2 * HIT_IMPULSE_FACTOR * v_magnitude2
                    ball2.acceleration[1] -= ny2 * HIT_IMPULSE_FACTOR * v_magnitude2

                # Actualizar cooldown
                game.hit_cooldowns[pair_key] = current_time

            # Chequear daño: arma2 toca ball1
            if circle_line_intersection(ball1.position, BALL_RADIUS, weapon2_start, weapon2_end):
                damage = ball2.weapon.calculate_damage()
                ball1.apply_damage(damage)
                ball2.weapon.on_hit()
                # Impulso para atacante (ball2 hacia atrás)
                v_magnitude2 = math.sqrt(ball2.base_velocity[0]**2 + ball2.base_velocity[1]**2)
                if v_magnitude2 > 0:
                    nx2 = ball2.base_velocity[0] / v_magnitude2
                    ny2 = ball2.base_velocity[1] / v_magnitude2
                    ball2.acceleration[0] -= nx2 * HIT_IMPULSE_FACTOR * v_magnitude2
                    ball2.acceleration[1] -= ny2 * HIT_IMPULSE_FACTOR * v_magnitude2

                # Impulso para atacada (ball1 hacia delante, reverse)
                v_magnitude1 = math.sqrt(ball1.base_velocity[0]**2 + ball1.base_velocity[1]**2)
                if v_magnitude1 > 0:
                    nx1 = ball1.base_velocity[0] / v_magnitude1
                    ny1 = ball1.base_velocity[1] / v_magnitude1
                    ball1.acceleration[0] -= nx1 * HIT_IMPULSE_FACTOR * v_magnitude1
                    ball1.acceleration[1] -= ny1 * HIT_IMPULSE_FACTOR * v_magnitude1

                # Actualizar cooldown
                game.hit_cooldowns[pair_key] = current_time