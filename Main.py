import pygame
from classes import *
from process import process

pygame.init()

resolution = [360, 480]
screen = pygame.display.set_mode(resolution, 0, 32)

clock = pygame.time.Clock()
fps = 60

# Instances
player = Player(100, resolution[1] - 50, 20, 18, 'resources/player.png')

background = pygame.image.load('resources/space_map.png')

while True:
	process(player)
	# logic
	player.motion(resolution)
	# end logic

	# drawing
	screen.fill((0, 255, 0))
	# screen.blit(background, background.get_rect())
	BaseClass.Sprites.draw(screen)
	pygame.display.flip()
	# end drawing
	clock.tick(fps)