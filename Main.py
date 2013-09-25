import pygame
from classes import Application

pygame.init()

app = Application('SpaceX', [360, 480], 60)

app.run()