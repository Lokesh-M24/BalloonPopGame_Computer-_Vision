# utils.py

import pygame
import random

class Balloon:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = random.randint(2, 5)

    def move(self):
        self.rect.y -= self.speed
        if self.rect.y < -100:
            self.rect.y = 720 + random.randint(50, 150)
            self.rect.x = random.randint(100, 1100)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
