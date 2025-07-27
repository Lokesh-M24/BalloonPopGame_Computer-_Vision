# Interactive Wall Projection Balloon Pop Game
# Simulates touch interaction using webcam + hand detection

import pygame
import cv2
import numpy as np
import time
import random
import os
import sys
from utils import map_coordinates, check_collision

# Initialize pygame
pygame.init()

# Set up fullscreen display for wall projection
infoObject = pygame.display.Info()
WIDTH, HEIGHT = infoObject.current_w, infoObject.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Interactive Wall Balloon Pop")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 102, 204)
GREEN = (0, 200, 0)

# Load assets
current_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(current_dir, "assets")

# Load background images
background_img = pygame.transform.scale(pygame.image.load(os.path.join(assets_dir, "BackgroundBlue.jpg")), (WIDTH, HEIGHT))
gameover_img = pygame.transform.scale(pygame.image.load(os.path.join(assets_dir, "background.png")), (WIDTH, HEIGHT))

# Load balloon images
def load_balloon(filename):
    return pygame.transform.scale(pygame.image.load(os.path.join(assets_dir, filename)), (80, 100))

balloon_images = {
    "red": load_balloon("BalloonRed.png"),
    "yellow": load_balloon("BalloonYellow.png"),
    "green": load_balloon("BalloonGreen.png"),
    "bomb": load_balloon("BalloonBomb.png"),
    "gold": load_balloon("BalloonGold.png")
}

# Load font
try:
    font_path = os.path.join(assets_dir, "Marcellus-Regular.ttf")
    score_font = pygame.font.Font(font_path, 36)
    game_over_font = pygame.font.Font(font_path, 64)
    pop_font = pygame.font.Font(font_path, 28)
except:
    score_font = pygame.font.SysFont(None, 36)
    game_over_font = pygame.font.SysFont(None, 64)
    pop_font = pygame.font.SysFont(None, 28)

# Webcam setup (camera must face projection screen)
# cap = cv2.VideoCapture("http://192.168.29.26:4747/video")
cap = cv2.VideoCapture(0)
from cvzone.HandTrackingModule import HandDetector
detector = HandDetector(detectionCon=0.8, maxHands=1)

class Balloon:
    def __init__(self):
        self.reset()
        self.popped = False
        self.pop_time = 0
        self.pop_effect = ""

    def reset(self):
        self.color = random.choices(["red", "yellow", "green", "bomb", "gold"], weights=[0.35, 0.2, 0.2, 0.15, 0.1])[0]
        self.image = balloon_images[self.color]
        self.x = random.randint(100, WIDTH - 100)
        self.y = HEIGHT + random.randint(50, 200)
        self.speed = random.uniform(1.5, 3.5)
        self.popped = False
        self.pop_effect = ""

    def update(self):
        if not self.popped:
            self.y -= self.speed
            if self.y < -100:
                self.reset()
        elif time.time() - self.pop_time > 0.5:
            self.reset()

    def draw(self, surface):
        if not self.popped:
            rect = self.image.get_rect(center=(self.x, self.y))
            surface.blit(self.image, rect)
            return rect
        else:
            elapsed = time.time() - self.pop_time
            scale = 1 - (elapsed / 0.5)
            size = int(80 * scale), int(100 * scale)
            temp_img = pygame.transform.scale(self.image, size)
            temp_img.set_alpha(int(255 * scale))
            rect = temp_img.get_rect(center=(self.x, self.y))
            surface.blit(temp_img, rect)
            if self.pop_effect:
                color = RED if '-' in self.pop_effect else GREEN
                label = pop_font.render(self.pop_effect, True, color)
                screen.blit(label, (self.x - 20, self.y - 50))
            return rect

    def pop(self):
        self.popped = True
        self.pop_time = time.time()


def smooth_hand_tracking(prev_pos, new_pos, alpha=0.3):
    if not prev_pos:
        return new_pos
    x = int(prev_pos[0] * (1 - alpha) + new_pos[0] * alpha)
    y = int(prev_pos[1] * (1 - alpha) + new_pos[1] * alpha)
    return (x, y)


def main():
    balloons = [Balloon() for _ in range(6)]
    score = 0
    start_time = time.time()
    game_time = 30
    game_over = False
    running = True
    last_pops = []
    fingertip_pos = None
    prev_pos = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r and game_over:
                main()
                return

        elapsed_time = time.time() - start_time
        time_left = max(0, game_time - elapsed_time)

        if time_left <= 0 and not game_over:
            game_over = True
            snapshot = cv2.flip(cap.read()[1], 1)
            cv2.imwrite("snapshot.png", snapshot)
            with open("leaderboard.txt", "a") as f:
                f.write(f"{score}\n")

        success, img = cap.read()
        img = cv2.flip(img, 1)
        hands, img = detector.findHands(img, flipType=False)

        if hands and not game_over:
            x, y = hands[0]['lmList'][8][0:2]
            new_pos = map_coordinates((x, y), img.shape, (WIDTH, HEIGHT))
            fingertip_pos = smooth_hand_tracking(prev_pos, new_pos)
            prev_pos = fingertip_pos

        screen.blit(background_img if not game_over else gameover_img, (0, 0))

        if not game_over:
            for balloon in balloons:
                balloon.update()
                rect = balloon.draw(screen)
                if fingertip_pos and not balloon.popped and check_collision(fingertip_pos, rect):
                    balloon.pop()
                    if balloon.color == "red":
                        score += 5
                        balloon.pop_effect = "+5"
                    elif balloon.color == "yellow":
                        score += 10
                        balloon.pop_effect = "+10"
                    elif balloon.color == "green":
                        score += 15
                        balloon.pop_effect = "+15"
                    elif balloon.color == "bomb":
                        score -= 10
                        balloon.pop_effect = "-10"
                    elif balloon.color == "gold":
                        score += 20
                        balloon.pop_effect = "+20"

            score_text = score_font.render(f"Score: {score}", True, BLACK)
            time_label = score_font.render("Time:", True, BLACK)
            time_value = score_font.render(f"{int(time_left)}s", True, RED)
            screen.blit(score_text, (10, 10))
            screen.blit(time_label, (WIDTH - 150, 10))
            screen.blit(time_value, (WIDTH - 70, 10))
        else:
            over = game_over_font.render("Game Over!", True, BLUE)
            final = score_font.render(f"Final Score: {score}", True, BLUE)
            restart = score_font.render("Press R to Restart or Q to Quit", True, BLUE)
            screen.blit(over, (WIDTH//2 - over.get_width()//2, HEIGHT//2 - 100))
            screen.blit(final, (WIDTH//2 - final.get_width()//2, HEIGHT//2))
            screen.blit(restart, (WIDTH//2 - restart.get_width()//2, HEIGHT//2 + 60))

        if fingertip_pos and not game_over:
            pygame.draw.circle(screen, RED, fingertip_pos, 15)
            pygame.draw.circle(screen, WHITE, fingertip_pos, 5)

        pygame.display.flip()
        cv2.imshow("Webcam", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    pygame.quit()

if __name__ == "__main__":
    main()