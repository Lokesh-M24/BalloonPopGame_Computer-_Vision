import cv2
import pygame
import random
import time
from utils import Balloon
from ball_detector import BallDetector
import mediapipe as mp

# --- Init ---
pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Interactive Balloon Pop")
clock = pygame.time.Clock()

# --- Load Assets ---
bg_img = pygame.image.load("assets/background.png")
bg_img = pygame.transform.scale(bg_img, (1280, 720))
pop_sound = pygame.mixer.Sound("assets/pop.wav.mp3")  # MUST be .wav format

balloon_images = [
    pygame.transform.scale(pygame.image.load("assets/BalloonRed.png"), (80, 120)),
    pygame.transform.scale(pygame.image.load("assets/BalloonGreen.png"), (80, 120)),
    pygame.transform.scale(pygame.image.load("assets/BalloonYellow.png"), (80, 120)),
    pygame.transform.scale(pygame.image.load("assets/BalloonGold.png"), (80, 120)),
    pygame.transform.scale(pygame.image.load("assets/BalloonBomb.png"), (80, 120))
]

# --- Camera (use laptop or mobile IP camera) ---
cap = cv2.VideoCapture("http://192.168.29.103:4747/video")  # Replace with 0 if using laptop webcam

# --- Detection Setup ---
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=2, min_detection_confidence=0.7)
ball_detector = BallDetector("models/yolov8n.pt")

# --- Game Settings ---
font = pygame.font.SysFont("Arial", 36)
score = 0
game_duration = 30  # seconds
start_time = time.time()

# --- Balloons ---
balloons = []
for _ in range(5):
    x = random.randint(100, 1100)
    y = random.randint(500, 700)
    img = random.choice(balloon_images)
    balloons.append(Balloon(x, y, img))

# --- Functions ---
def detect_hand(frame):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(frame_rgb)
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            index_finger = hand_landmarks.landmark[8]
            x = int(index_finger.x * 1280)
            y = int(index_finger.y * 720)
            return (x, y)
    return None

def draw_score(scr, val):
    text = font.render(f"Score: {val}", True, (0, 0, 0))
    scr.blit(text, (20, 20))

def draw_timer(scr, secs):
    text = font.render(f"Time Left: {int(secs)}s", True, (255, 0, 0))
    scr.blit(text, (1000, 20))

def reset_game():
    global balloons, score, start_time
    score = 0
    start_time = time.time()
    balloons = []
    for _ in range(5):
        x = random.randint(100, 1100)
        y = random.randint(500, 700)
        img = random.choice(balloon_images)
        balloons.append(Balloon(x, y, img))

# --- Game Loop ---
running = True
while running:
    success, frame = cap.read()
    if not success:
        continue
    frame = cv2.flip(frame, 1)

    hand_pos = detect_hand(frame)
    balls = ball_detector.detect_balls(frame)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
            if event.key == pygame.K_r:
                reset_game()

    screen.blit(bg_img, (0, 0))

    for balloon in balloons[:]:
        balloon.move()
        balloon.draw(screen)

        # Hand Touch
        if hand_pos:
            hx, hy = hand_pos
            pygame.draw.circle(screen, (255, 0, 0), (hx, hy), 10)
            if balloon.rect.collidepoint((hx, hy)):
                balloons.remove(balloon)
                new_img = random.choice(balloon_images)
                balloons.append(Balloon(random.randint(100, 1100), 700, new_img))
                score += 5
                pop_sound.play()

        # Ball Hit
        for ball in balls:
            cx, cy = ball["center"]
            if balloon.rect.collidepoint((cx, cy)):
                balloons.remove(balloon)
                new_img = random.choice(balloon_images)
                balloons.append(Balloon(random.randint(100, 1100), 700, new_img))
                score += 10
                pop_sound.play()

    # UI
    time_left = game_duration - (time.time() - start_time)
    draw_score(screen, score)
    draw_timer(screen, time_left)

    pygame.display.update()
    clock.tick(60)

    if time_left <= 0:
        running = False

# --- End Screen ---
screen.fill((255, 255, 255))
end_text = font.render(f"Game Over! Your Score: {score}", True, (0, 0, 128))
screen.blit(end_text, (400, 350))
pygame.display.update()
pygame.time.delay(5000)

cap.release()
pygame.quit()
