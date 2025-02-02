import pygame
import math
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions and setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Ball properties
ball_radius = 15
ball_x = WIDTH // 2
ball_y = HEIGHT // 3
ball_dx = 3  # Horizontal velocity
ball_dy = 0  # Vertical velocity

# Physics constants
gravity = 0.5
friction = 0.98
bounciness = 0.75

# Hexagon properties
hexagon_center = (WIDTH // 2, HEIGHT // 2)
hexagon_radius = 200
hexagon_angle = 0
hexagon_angular_velocity = 1  # Degrees per frame

# Function to calculate hexagon vertices
def get_hexagon_points(center, radius, rotation_angle):
    cx, cy = center
    points = []
    for i in range(6):
        angle_deg = 60 * i + rotation_angle
        angle_rad = math.radians(angle_deg)
        x = cx + radius * math.cos(angle_rad)
        y = cy + radius * math.sin(angle_rad)
        points.append((x, y))
    return points

# Function to reflect the ball off a line segment
def reflect_ball(ball_pos, ball_velocity, wall_start, wall_end):
    bx, by = ball_pos
    vx, vy = ball_velocity

    # Wall vector and normal vector
    wx, wy = wall_end[0] - wall_start[0], wall_end[1] - wall_start[1]
    wall_length = math.hypot(wx, wy)
    wx /= wall_length
    wy /= wall_length

    # Normal vector perpendicular to the wall
    nx, ny = -wy, wx

    # Vector from wall_start to ball
    px, py = bx - wall_start[0], by - wall_start[1]

    # Projection of the ball's velocity onto the normal
    dot_product = vx * nx + vy * ny

    # Reflect the ball velocity
    vx -= 2 * dot_product * nx
    vy -= 2 * dot_product * ny

    # Apply bounciness and friction
    vx *= bounciness
    vy *= bounciness
    return vx, vy

# Main game loop
running = True
while running:
    screen.fill(BLACK)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update ball position
    ball_dy += gravity  # Apply gravity
    ball_x += ball_dx
    ball_y += ball_dy

    # Update hexagon rotation
    hexagon_angle = (hexagon_angle + hexagon_angular_velocity) % 360
    hexagon_points = get_hexagon_points(hexagon_center, hexagon_radius, hexagon_angle)

    # Draw hexagon
    pygame.draw.polygon(screen, WHITE, hexagon_points, 2)

    # Draw ball
    pygame.draw.circle(screen, RED, (int(ball_x), int(ball_y)), ball_radius)

    # Collision detection and response
    for i in range(6):
        start_point = hexagon_points[i]
        end_point = hexagon_points[(i + 1) % 6]

        # Check for collision with each hexagon edge
        wall_dx = end_point[0] - start_point[0]
        wall_dy = end_point[1] - start_point[1]
        wall_length = math.hypot(wall_dx, wall_dy)
        
        if wall_length == 0:
            continue

        # Normalize wall vector
        wall_dx /= wall_length
        wall_dy /= wall_length

        # Check distance to wall segment
        px = ball_x - start_point[0]
        py = ball_y - start_point[1]

        projection = px * wall_dx + py * wall_dy

        if 0 <= projection <= wall_length:
            nearest_x = start_point[0] + projection * wall_dx
            nearest_y = start_point[1] + projection * wall_dy

            distance = math.hypot(ball_x - nearest_x, ball_y - nearest_y)

            if distance <= ball_radius:
                ball_dx, ball_dy = reflect_ball((ball_x, ball_y), (ball_dx, ball_dy), start_point, end_point)

    # Bounce off screen edges
    if ball_x - ball_radius < 0 or ball_x + ball_radius > WIDTH:
        ball_dx *= -1
    if ball_y - ball_radius < 0 or ball_y + ball_radius > HEIGHT:
        ball_dy *= -1

    # Apply friction
    ball_dx *= friction
    ball_dy *= friction

    # Update the display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
