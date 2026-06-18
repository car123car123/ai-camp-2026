#!/usr/bin/env python3
import math
import random
import sys
import pygame

# ---------------- CONFIG ----------------
SCREEN_W, SCREEN_H = 1280, 720
FPS = 60

CAR_IMG = "supra.png"
TRAFFIC_IMG = "skyra.png"

LANE_COUNT = 4
LANE_WIDTH = 50
LANE_GAP = 10

ROAD_GAP = 200

CAR_MAX_SPEED = 420.0
CAR_ACCEL = 900.0
CAR_STEER_RATE = 3.5

FRICTION = 2.5  # better than exponential hack

TRAFFIC_COUNT = 8

# Colors
ROAD = (50, 50, 50)
LANE = (220, 220, 220)
BUILDING = (70, 70, 120)
NIGHT = (10, 10, 30)

WEATHER = {
    "Clear": (135, 206, 235),
    "Rain": (90, 110, 120),
    "Fog": (200, 200, 200),
}

# ---------------- ROAD GEOMETRY ----------------
ROAD_W = LANE_COUNT * LANE_WIDTH + (LANE_COUNT - 1) * LANE_GAP

LEFT_X = SCREEN_W * 0.25
RIGHT_X = SCREEN_W * 0.75

LEFT_MIN = LEFT_X - ROAD_W / 2
LEFT_MAX = LEFT_X + ROAD_W / 2
RIGHT_MIN = RIGHT_X - ROAD_W / 2
RIGHT_MAX = RIGHT_X + ROAD_W / 2


# ---------------- HELPERS ----------------
def load_img(path, size=(40, 20)):
    try:
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, size)
    except:
        surf = pygame.Surface(size, pygame.SRCALPHA)
        surf.fill((255, 0, 0))
        return surf


# ---------------- CAR ----------------
class Car:
    def __init__(self, pos, img):
        self.pos = pygame.Vector2(pos)
        self.angle = math.pi / 2
        self.speed = 0
        self.img = img

    def accelerate(self, dt, forward):
        self.speed += (CAR_ACCEL * dt) * (1 if forward else -1)
        self.speed = max(-60, min(CAR_MAX_SPEED, self.speed))

    def steer(self, dt, direction):
        # smoother steering (less jitter)
        self.angle += direction * CAR_STEER_RATE * dt * (self.speed / CAR_MAX_SPEED)

    def update(self, dt, bounds):
        forward = pygame.Vector2(math.cos(self.angle), math.sin(self.angle))
        self.pos += forward * self.speed * dt

        # friction (stable linear damping)
        self.speed -= self.speed * FRICTION * dt

        # keep inside road
        min_x, max_x = bounds
        if self.pos.x < min_x:
            self.pos.x = min_x
            self.speed *= -0.3
        if self.pos.x > max_x:
            self.pos.x = max_x
            self.speed *= -0.3

        self.pos.y = max(0, min(SCREEN_H, self.pos.y))

    def draw(self, screen):
        rot = pygame.transform.rotate(self.img, -math.degrees(self.angle))
        rect = rot.get_rect(center=self.pos)
        screen.blit(rot, rect.topleft)


# ---------------- BUILDINGS ----------------
def buildings():
    b = []
    for x in (LEFT_MIN - 100, RIGHT_MAX + 100):
        for _ in range(4):
            h = random.randint(150, 400)
            y = random.randint(0, SCREEN_H - h)
            b.append(pygame.Rect(x, y, 80, h))
    return b


# ---------------- MAIN ----------------
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    clock = pygame.time.Clock()

    player = Car((LEFT_X, SCREEN_H / 2), load_img(CAR_IMG))
    npc = Car((RIGHT_X, SCREEN_H / 3), load_img(TRAFFIC_IMG))

    traffic = []
    traffic_on = False

    weather = "Clear"
    day = True

    blds = buildings()

    def bg():
        return NIGHT if not day else WEATHER[weather]

    running = True
    while running:
        dt = clock.tick(FPS) / 1000

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

            if e.type == pygame.KEYDOWN:
                # FIX: avoid W conflict by using Q for weather
                if e.key == pygame.K_q:
                    weather = {"Clear": "Rain", "Rain": "Fog", "Fog": "Clear"}[weather]

                if e.key == pygame.K_e:
                    day = not day

                if e.key == pygame.K_t:
                    traffic_on = not traffic_on
                    traffic.clear()
                    if traffic_on:
                        for _ in range(TRAFFIC_COUNT):
                            traffic.append(
                                Car(
                                    (random.uniform(RIGHT_MIN, RIGHT_MAX),
                                     random.uniform(100, SCREEN_H - 100)),
                                    load_img(TRAFFIC_IMG),
                                )
                            )

        keys = pygame.key.get_pressed()

        # movement
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player.accelerate(dt, True)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player.accelerate(dt, False)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.steer(dt, -1)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.steer(dt, 1)

        # update
        player.update(dt, (LEFT_MIN, LEFT_MAX))
        npc.update(dt, (RIGHT_MIN, RIGHT_MAX))

        for c in traffic:
            c.update(dt, (RIGHT_MIN, RIGHT_MAX))

        # draw
        screen.fill(bg())

        pygame.draw.rect(screen, ROAD, (LEFT_MIN, 0, ROAD_W, SCREEN_H))
        pygame.draw.rect(screen, ROAD, (RIGHT_MIN, 0, ROAD_W, SCREEN_H))

        draw_y = 0
        while draw_y < SCREEN_H:
            pygame.draw.line(screen, LANE, (LEFT_X, draw_y), (LEFT_X, draw_y + 20), 2)
            pygame.draw.line(screen, LANE, (RIGHT_X, draw_y), (RIGHT_X, draw_y + 20), 2)
            draw_y += 35

        for r in blds:
            pygame.draw.rect(screen, BUILDING, r)

        player.draw(screen)
        npc.draw(screen)
        for c in traffic:
            c.draw(screen)

        font = pygame.font.SysFont(None, 24)
        txt = font.render(
            f"Traffic:{traffic_on} Weather:{weather} Day:{day}",
            True,
            (255, 255, 255),
        )
        screen.blit(txt, (10, 10))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
