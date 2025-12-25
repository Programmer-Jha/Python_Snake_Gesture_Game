# Developed By: Aniket Kumar Jha

import pygame
import cv2
import mediapipe as mp
import random
import numpy as np

pygame.init()

SCREEN_W, SCREEN_H = 1200, 600
CAM_W, GAME_W = 600, 600
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Gesture Snake Game")

clock = pygame.time.Clock()
FPS = 8

# Colors
BLACK = (0, 0, 0)
BLUE = (50, 153, 213)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
RED = (213, 50, 80)
WHITE = (255, 255, 255)

BLOCK = 10

mpHands = mp.solutions.hands
mpDraw = mp.solutions.drawing_utils

hands = mpHands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

cap = cv2.VideoCapture(0)

font = pygame.font.SysFont("comicsansms", 28)

def draw_text(text, color, x, y):
    screen.blit(font.render(text, True, color), (x, y))

def is_opposite(d1, d2):
    return (d1 == "UP" and d2 == "DOWN") or \
           (d1 == "DOWN" and d2 == "UP") or \
           (d1 == "LEFT" and d2 == "RIGHT") or \
           (d1 == "RIGHT" and d2 == "LEFT")

def new_food(snake):
    while True:
        food = [
            random.randrange(0, GAME_W // BLOCK) * BLOCK,
            random.randrange(0, SCREEN_H // BLOCK) * BLOCK
        ]
        if food not in snake:
            return food

def gameLoop():
    direction = "STOP"  
    snake = [[300, 300]]
    length = 1
    food = new_food(snake)  

    prev_pos = None
    gesture_cooldown = 0  
    game_over = False

    while not game_over:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        
        ret, frame = cap.read()
        if ret:
            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb)

            if results.multi_hand_landmarks:
                hand = results.multi_hand_landmarks[0]

                
                mpDraw.draw_landmarks(
                    frame,
                    hand,
                    mpHands.HAND_CONNECTIONS,
                    mpDraw.DrawingSpec(color=(0, 255, 255), thickness=2, circle_radius=4),
                    mpDraw.DrawingSpec(color=(255, 255, 0), thickness=2)
                )

                idx = hand.landmark[8]  
                h, w, _ = frame.shape
                curr = (int(idx.x * w), int(idx.y * h))

                if prev_pos and gesture_cooldown == 0:
                    dx = curr[0] - prev_pos[0]
                    dy = curr[1] - prev_pos[1]
                    TH = 30  

                    if abs(dx) > abs(dy):
                        if dx > TH and not is_opposite(direction, "RIGHT"):
                            direction = "RIGHT"
                        elif dx < -TH and not is_opposite(direction, "LEFT"):
                            direction = "LEFT"
                    else:
                        if dy > TH and not is_opposite(direction, "DOWN"):
                            direction = "DOWN"
                        elif dy < -TH and not is_opposite(direction, "UP"):
                            direction = "UP"

                    gesture_cooldown = 1  

                prev_pos = curr
            else:
                prev_pos = None

            if gesture_cooldown > 0:
                gesture_cooldown -= 1

            frame = cv2.resize(frame, (CAM_W, SCREEN_H))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = np.rot90(frame)
            frame = pygame.surfarray.make_surface(frame)
            screen.blit(frame, (0, 0))

        
        if direction != "STOP":
            head_x, head_y = snake[-1]

            if direction == "UP":
                head_y -= BLOCK
            elif direction == "DOWN":
                head_y += BLOCK
            elif direction == "LEFT":
                head_x -= BLOCK
            elif direction == "RIGHT":
                head_x += BLOCK

            new_head = [head_x, head_y]
            snake.append(new_head)

            if len(snake) > length:
                snake.pop(0)

            
            if (
                head_x < 0 or head_x >= GAME_W or
                head_y < 0 or head_y >= SCREEN_H or
                new_head in snake[:-1]
            ):
                game_over = True

            if new_head == food:
                length += 1
                food = new_food(snake)  

        
        pygame.draw.rect(screen, BLUE, (CAM_W, 0, GAME_W, SCREEN_H))

        pygame.draw.rect(
            screen, ORANGE,
            (CAM_W + food[0], food[1], BLOCK, BLOCK)
        )

        for block in snake:
            pygame.draw.rect(
                screen, GREEN,
                (CAM_W + block[0], block[1], BLOCK, BLOCK)
            )

        draw_text(f"Score: {length - 1}", WHITE, CAM_W + 20, 10)
        draw_text(f"Direction: {direction}", WHITE, CAM_W + 20, 40)

        pygame.display.update()
        clock.tick(FPS)

    screen.fill(BLACK)
    draw_text("GAME OVER", RED, SCREEN_W // 2 - 100, SCREEN_H // 2 - 40)
    draw_text("Press R to Restart or Q to Quit", WHITE, SCREEN_W // 2 - 180, SCREEN_H // 2)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    gameLoop()
                elif event.key == pygame.K_q:
                    return
            if event.type == pygame.QUIT:
                return

gameLoop()
cap.release()
pygame.quit()